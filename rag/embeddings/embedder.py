"""
rag/embeddings/embedder.py

Single call-site for the embedding function used to index and query
the job-postings vector store. Chroma ships a default local embedding
function (all-MiniLM-L6-v2, run on-device via onnxruntime) which needs
no API key -- that's what we use by default, matching the "free tier
by default" approach the rest of the project takes (agents/config.py's
LLM_PROVIDER=groq default). If a project later wants OpenAI/Cohere
embeddings, swap the implementation here; nothing in
rag/vectorstore or rag/retrieval needs to change.
"""

import logging

logger = logging.getLogger(__name__)

_cached_embedding_function = None


def get_embedding_function():
    """Returns a chromadb-compatible embedding function. Cached after
    first call since loading the underlying model has a fixed cost.
    Returns None if the dependency isn't installed / reachable, in
    which case callers should fall back to Chroma's own default
    (letting `get_or_create_collection` omit embedding_function) or to
    a non-vector retrieval path."""
    global _cached_embedding_function
    if _cached_embedding_function is not None:
        return _cached_embedding_function

    try:
        from chromadb.utils import embedding_functions
        _cached_embedding_function = embedding_functions.DefaultEmbeddingFunction()
        return _cached_embedding_function
    except Exception as e:
        logger.warning(f"Could not load default embedding function: {e}")
        return None
