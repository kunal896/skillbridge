# SkillBridge

AI-powered workforce reskilling platform for the AGENTRIX 2026 hackathon.

## MVP flow

Learner profile / resume
→ skill-gap diagnosis
→ RAG-grounded roadmap
→ cited job postings
→ micro-project
→ sandboxed verification
→ unlocked skill tree
→ employer matching

## Repository structure

- `frontend/` — Next.js + Tailwind UI
- `backend/` — FastAPI API, database and business services
- `agents/` — LangGraph diagnosis, roadmap and verification agents
- `rag/` — job-posting ingestion, embeddings and retrieval
- `matching/` — learner/employer matching
- `shared/` — contracts shared between modules
- `data/` — seed and demo data
- `docs/` — architecture, API, setup and demo notes
- `scripts/` — developer utilities

## Team rule

Each person owns a module. Avoid editing another person's module unless the team agrees first.

Before coding, agree on the contracts in `shared/contracts/`. If a module needs a different input/output shape, update the contract first and tell the team.

## Git rule

Never work directly on `main`.

Use one feature branch per task:

    git checkout -b feature/your-task

Commit small, meaningful changes:

    git add .
    git commit -m "feat: add diagnosis contract"

Push the branch and open a Pull Request into `main`.

## First setup

1. Copy `.env.example` to `.env`.
2. Install frontend/backend dependencies when those modules are initialized.
3. Start PostgreSQL with Docker when the database setup is added.
4. Read `docs/setup.md`.

## Current status

This repository is the architecture/foundation skeleton. Feature implementation comes next.
