"""
rag/

Owns (per docs/module-boundaries.md): job ingestion, normalization,
embeddings, retrieval, citation metadata.

Public surface other modules should import:
    from rag.retrieval import retrieve_postings
    from rag.ingestion import fetch_postings, ingest

Nothing outside rag/ should reach into rag.vectorstore or
rag.embeddings directly -- go through rag.retrieval / rag.ingestion so
the storage/embedding backend can change without touching callers
(agents/, backend/).
"""
