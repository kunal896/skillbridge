"""
rag/vectorstore/chroma_store.py

Thin wrapper around a persistent Chroma collection of normalized job
postings (see rag/normalization). This is the only place in the
codebase that should import chromadb directly -- agents/tools.py used
to do this inline, which is exactly the kind of module-boundary
crossing docs/module-boundaries.md warns against ("rag/ owns ...
retrieval"). agents/ now goes through rag.retrieval instead.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .. import config
from ..embeddings.embedder import get_embedding_function

logger = logging.getLogger(__name__)


class ChromaJobStore:
    def __init__(self, persist_dir: Optional[str] = None, collection_name: Optional[str] = None):
        self.persist_dir = str((Path(__file__).resolve().parents[2] / config.CHROMA_PERSIST_DIR).resolve()) if not Path(config.CHROMA_PERSIST_DIR).is_absolute() else config.CHROMA_PERSIST_DIR
        self.collection_name = collection_name or config.CHROMA_COLLECTION_NAME
        self._client = None
        self._collection = None

    def _get_collection(self):
        if self._collection is not None:
            return self._collection

        import chromadb

        self._client = chromadb.PersistentClient(path=self.persist_dir)
        embedding_fn = get_embedding_function()
        kwargs: Dict[str, Any] = {"name": self.collection_name}
        if embedding_fn is not None:
            kwargs["embedding_function"] = embedding_fn
        self._collection = self._client.get_or_create_collection(**kwargs)
        return self._collection

    def count(self) -> int:
        try:
            return self._get_collection().count()
        except Exception as e:
            logger.warning(f"ChromaDB unavailable when counting: {e}")
            return 0

    def upsert(self, postings: List[Dict[str, Any]]) -> int:
        """Upsert normalized JobPosting records (see
        rag.normalization.normalize_posting). Returns the number
        written."""
        if not postings:
            return 0

        collection = self._get_collection()
        ids = [p["job_id"] for p in postings]
        documents = [f"{p['title']}\n{p['description']}" for p in postings]
        metadatas = [
            {
                "title": p.get("title", ""),
                "company": p.get("company") or "",
                "location": p.get("location") or "",
                "region": p.get("region") or "",
                "source_name": p.get("source_name", "sample"),
                "source_url": p.get("source_url", ""),
                "posted_at": p.get("posted_at") or "",
                "skills": ",".join(p.get("skills", [])),
            }
            for p in postings
        ]
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        return len(ids)

    def query(self, query_text: str, top_k: int) -> List[Dict[str, Any]]:
        collection = self._get_collection()
        if collection.count() == 0:
            return []

        results = collection.query(query_texts=[query_text], n_results=top_k)

        postings: List[Dict[str, Any]] = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        for idx, (doc, meta, dist) in enumerate(zip(docs, metas, dists)):
            job_id = ids[idx] if idx < len(ids) else f"job_{idx + 1:03d}"
            skills = meta.get("skills", "")
            postings.append({
                "job_id": job_id,
                "title": meta.get("title", "Job Posting"),
                "company": meta.get("company") or None,
                "location": meta.get("location") or None,
                "text": doc,
                "source_name": meta.get("source_name", "Job Vector DB"),
                "source_url": meta.get("source_url", f"https://example.com/jobs/{job_id}"),
                "posted_at": meta.get("posted_at") or None,
                "skills": skills.split(",") if skills else [],
                # Chroma returns a distance (lower = closer); convert to a
                # 0-1 "relevance score" (higher = better) for citations.
                "score": 1 - dist if isinstance(dist, (int, float)) else 0.5,
            })
        return postings
