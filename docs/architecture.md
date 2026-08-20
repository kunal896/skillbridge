# SkillBridge Architecture

## High-level flow

Frontend
→ FastAPI backend
→ LangGraph orchestration
→ Diagnosis / Roadmap / Verification agents
→ RAG + job data / Judge0
→ PostgreSQL
→ Frontend output

## Module ownership

| Module | Primary owner |
|---|---|
| `agents/` | Kunal |
| `rag/` | Kunal |
| `backend/` | Vinod |
| `matching/` | Abhignya |
| `frontend/` | Kunal + Suchi |
| `shared/` | Everyone, changes must be agreed |
| QA / tests | Suchi |

## Important rule

The modules communicate through explicit contracts. Do not silently change a contract used by another module.
