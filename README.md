# SkillBridge

> AI-powered workforce reskilling platform — built for **AGENTRIX 2026**.

Most reskilling tools recommend from a fixed course catalogue and treat *"completed the course"* as proof of skill. **SkillBridge is different:** every recommendation is grounded in live job-posting data, and no skill unlocks until a graded submission passes verification.

---

## How it works

```
Learner resume / MCQ
      │
      ▼  skill-gap diagnosis
      ▼  RAG-grounded, cited roadmap  (every step traces to a real job posting)
      ▼  micro-project per skill node
      ▼  sandboxed + LLM-judge verification
      ▼  unlocked skill tree
      ▼  employer matching
```

Nothing on the roadmap is asserted without a source. Nothing on the skill tree unlocks without a passed, graded submission.

---

## Repository layout

| Module        | Responsibility                                          |
| ------------- | ------------------------------------------------------- |
| `frontend/`   | Next.js + Tailwind — pages, components, skill-tree UI   |
| `backend/`    | FastAPI + PostgreSQL — HTTP API, auth, persistence      |
| `agents/`     | LangGraph — diagnosis, roadmap, verification            |
| `rag/`        | Job ingestion, embeddings, retrieval, citations         |
| `matching/`   | Learner ↔ employer scoring and match explanation        |
| `shared/`     | Contracts, types, and system-wide constants             |
| `data/`       | Sample / seed data                                      |
| `docs/`       | Project agreements and architecture                     |

---

## Getting started

**Read these first, in order:**

1. [`docs/shared-contracts.md`](docs/shared-contracts.md)
2. [`docs/module-boundaries.md`](docs/module-boundaries.md)
3. [`docs/git-workflow.md`](docs/git-workflow.md)

Then copy `.env.example` to `.env` and add your local secrets.

> ⚠️ **Never edit another person's module without agreement.**

---

## Quick demo run

```bash
# 1. Environment
cp .env.example .env          # then fill in your local secrets

# 2. Database
docker compose up -d postgres

# 3. Python deps (inside a venv)
pip install -r requirements.txt

# 4. Set PYTHONPATH (PowerShell — adjust for your shell)
$env:PYTHONPATH = ".;backend"

# 5. Migrations
alembic -c backend/alembic.ini upgrade head

# 6. Start the API
python -m uvicorn app.main:app --app-dir backend --reload --port 8000

# 7. Frontend (in frontend/)
npm install
npm run dev
```

Keep `NEXT_PUBLIC_USE_MOCKS=false` for the real backend demo.

> 💡 **Real verification** needs a reachable **Judge0** instance plus an LLM judge. Without both, verification *fails closed* — roadmap nodes stay locked rather than unlocking optimistically.

---

## The rule of the repo

AI tools can build each module independently — that's the whole point of the module split.
**Shared contracts are the agreement that keeps those independently-generated modules connecting.** The contract is the interface; module internals are free to be rebuilt as long as they keep speaking it.
