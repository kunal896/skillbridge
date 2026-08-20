# SkillBridge

AI-powered workforce reskilling platform for AGENTRIX 2026.

## MVP

Learner resume/MCQ
→ skill-gap diagnosis
→ RAG-grounded cited roadmap
→ micro-project
→ sandboxed verification
→ unlocked skill tree
→ employer matching

## Team modules

- `frontend/` — Next.js + Tailwind
- `backend/` — FastAPI + PostgreSQL
- `agents/` — LangGraph diagnosis, roadmap and verification
- `rag/` — job ingestion, embeddings and retrieval
- `matching/` — employer/learner matching
- `shared/` — contracts, types and constants
- `data/` — sample/seed data
- `docs/` — project agreements and architecture

## Start here

1. Read `docs/shared-contracts.md`.
2. Read `docs/module-boundaries.md`.
3. Read `docs/git-workflow.md`.
4. Copy `.env.example` to `.env`.
5. Do not edit another person's module without agreement.

## Rule of the repo

AI tools can write different modules independently.
Shared contracts are the agreement that makes those modules connect.


## Quick demo run

1. Copy `.env.example` to `.env` and add your local secrets.
2. Start PostgreSQL: `docker compose up -d postgres`.
3. Create/activate a Python venv and run `pip install -r requirements.txt`.
4. From the repo root set `PYTHONPATH=.;backend` in PowerShell.
5. Run migrations: `alembic -c backend/alembic.ini upgrade head`.
6. Start API: `python -m uvicorn app.main:app --app-dir backend --reload --port 8000`.
7. In `frontend/`, run `npm install` then `npm run dev`.
8. Keep `NEXT_PUBLIC_USE_MOCKS=false` for the real backend demo.

For real verification passes, configure a reachable Judge0 instance. Without Judge0 and an LLM judge, verification fails closed and does not unlock roadmap nodes.
