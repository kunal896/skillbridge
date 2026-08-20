from __future__ import annotations
from typing import Any
from .. import config
from ..vectorstore.chroma_store import ChromaJobStore

def _ensure_chroma_seed(query: str, top_k: int) -> None:
    store = ChromaJobStore()
    if store.count() > 0:
        return
    from ..ingestion.run_ingest import ingest
    ingest(roles=[query], limit_per_role=max(top_k, 10))

def retrieve_postings(query: str, top_k: int | None = None) -> list[dict[str, Any]]:
    top_k = top_k or config.RAG_TOP_K
    if config.VECTOR_STORE_BACKEND == "chroma":
        _ensure_chroma_seed(query, top_k)
        return ChromaJobStore().query(query, top_k)
    if config.VECTOR_STORE_BACKEND == "pinecone":
        from ..vectorstore.pinecone_store import PineconeJobStore
        return PineconeJobStore().query(query, top_k)
    raise ValueError(f"Unsupported VECTOR_STORE_BACKEND={config.VECTOR_STORE_BACKEND!r}")
