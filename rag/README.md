# RAG

Job-posting ingestion, normalization, embeddings, retrieval and
citation metadata. Owned by Kunal.

## What's here

```
rag/
  config.py                    env-driven settings (own copy, doesn't import agents/)
  ingestion/
    providers.py                fetch_postings() -- Adzuna if configured, else sample dataset
    sample_postings.py          bundled offline dataset spanning 8 target roles
    run_ingest.py                fetch -> normalize -> embed -> upsert pipeline (CLI + importable)
  normalization/
    normalize.py                 raw provider shape -> canonical JobPosting (shared/contracts/job_posting.json)
  embeddings/
    embedder.py                   single call-site for the embedding function (Chroma's local MiniLM by default)
  vectorstore/
    chroma_store.py               persistent Chroma collection: upsert / query
    pinecone_store.py             optional Pinecone backend (stubbed, opt-in)
  retrieval/
    retriever.py                  retrieve_postings(query, top_k) -- the ONLY public entry point
```

## Public API

Everything outside `rag/` should import from `rag.retrieval` (and
`rag.ingestion` for the CLI), not reach into `rag.vectorstore` or
`rag.embeddings` directly:

```python
from rag.retrieval import retrieve_postings

postings = retrieve_postings("Data Analyst SQL Excel", top_k=5)
# -> [{job_id, title, company, location, text, source_name,
#      source_url, posted_at, skills, score}, ...]
```

`agents/tools.py` calls this for roadmap grounding instead of talking
to Chroma directly (it used to -- that was a module-boundary
violation per `docs/module-boundaries.md`, which lists retrieval as
something `agents/` *consumes*, not owns).

## Running ingestion

By default (no `ADZUNA_APP_ID`/`ADZUNA_APP_KEY` set), ingestion pulls
from the bundled offline sample dataset covering 8 common target
roles (Data Analyst, Backend Engineer, Frontend Engineer, DevOps
Engineer, Machine Learning Engineer, Product Manager, QA Engineer,
UI/UX Designer) instead of a live API, so the pipeline works out of
the box with zero external accounts:

```bash
cd skillbridge
pip install -r rag/requirements.txt
python -m rag.ingestion.run_ingest
```

To use live Adzuna postings instead, set `ADZUNA_APP_ID` /
`ADZUNA_APP_KEY` in `.env` (get a free key at
https://developer.adzuna.com/) and re-run the same command -- no code
changes needed.

## Retrieval fallback behavior

If the vector store hasn't been populated yet (`python -m
rag.ingestion.run_ingest` hasn't been run), `retrieve_postings()`
still returns query-relevant results: it falls back to a
keyword-overlap ranking over the same bundled sample dataset rather
than a fixed, always-identical result set. This is why roadmap
citations vary by target role even before you've run ingestion --
run ingestion for real semantic (embedding-based) retrieval.

## Config (`.env` at repo root)

| Var | Default | Notes |
|---|---|---|
| `VECTOR_STORE_BACKEND` | `chroma` | `chroma` \| `pinecone` |
| `CHROMA_PERSIST_DIR` | `./data/chroma` | on-disk index location |
| `JOB_DATA_PROVIDER` | `adzuna` | falls back to sample data with no key |
| `ADZUNA_APP_ID` / `ADZUNA_APP_KEY` | _(empty)_ | free tier at developer.adzuna.com |
| `RAG_TOP_K` | `5` | default postings returned per query |
