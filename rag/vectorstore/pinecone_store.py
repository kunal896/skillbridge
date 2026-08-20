"""
rag/vectorstore/pinecone_store.py

Optional Pinecone-backed store, selected via VECTOR_STORE_BACKEND=pinecone.
Not required for local/free-tier development (chroma is the default --
see rag/config.py) -- this exists so switching backends later is a
config change, not a rewrite. Requires PINECONE_API_KEY.
"""

import logging
from typing import Any, Dict, List, Optional

from .. import config

logger = logging.getLogger(__name__)


class PineconeJobStore:
    def __init__(self, index_name: Optional[str] = None):
        self.index_name = index_name or config.PINECONE_INDEX_NAME
        self._index = None

    def _get_index(self):
        if self._index is not None:
            return self._index
        if not config.PINECONE_API_KEY:
            raise RuntimeError("PINECONE_API_KEY not set")

        from pinecone import Pinecone

        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        self._index = pc.Index(self.index_name)
        return self._index

    def upsert(self, postings: List[Dict[str, Any]]) -> int:
        # Pinecone requires vectors to be embedded by the caller (unlike
        # Chroma's built-in embedding function support). Left as a
        # documented extension point rather than guessed at, since the
        # project isn't using Pinecone by default -- wire in
        # rag.embeddings when this backend is actually adopted.
        raise NotImplementedError(
            "Pinecone upsert requires pre-computed embeddings; wire in "
            "rag.embeddings.get_embedding_function() here before use."
        )

    def query(self, query_text: str, top_k: int) -> List[Dict[str, Any]]:
        logger.info("Pinecone backend query requested but not fully wired; returning no results.")
        return []
