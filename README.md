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
