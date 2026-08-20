# SkillBridge Deployment Checklist

1. Set backend environment variables in the backend service.
2. Set `NEXT_PUBLIC_API_BASE_URL` to the public backend `/api/v1` URL.
3. Set `NEXT_PUBLIC_USE_MOCKS=false`.
4. Set `LLM_PROVIDER` and the corresponding API key.
5. Ensure Judge0 is reachable; never enable fake verification.
6. Set `DATABASE_URL` to the hosted PostgreSQL URL.
7. Run `alembic upgrade head` from `backend/`.
8. Run RAG ingestion once: `python -m rag.ingestion.run_ingest --roles "Data Analyst" "Backend Engineer"`.
9. Start backend: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` with working directory `backend/`.
10. Start frontend: `npm run build && npm start`.
11. Smoke test: register → create learner profile → diagnosis → roadmap → submit micro-project → verification history.
12. For employer demo: register employer → create requirement → request `/matches/employer/{employer_id}`.


## Employer demo

After employer login, create the employer profile via `PUT /api/v1/employers/me`, then create a requirement via `POST /api/v1/employers/requirements`. The requirement uses the shared `EmployerRequirement` shape. Request ranked results from `GET /api/v1/matches/employer/{employer_id}`.


## Demo reality check
- `NEXT_PUBLIC_USE_MOCKS=false` for real backend calls.
- `JUDGE0_BASE_URL` must point to a running Judge0 instance for a real verification pass.
- With no Judge0/LLM judge, verification remains fail-closed and does not unlock nodes.
- Sample RAG citations use the bundled sample dataset; do not present `example.com` as a live job source.
