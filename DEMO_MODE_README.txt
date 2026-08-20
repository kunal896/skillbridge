SKILLBRIDGE DEMO MODE
======================

This build is configured for a presentation/demo:
- Frontend API calls use deterministic mock data.
- Diagnosis works without an LLM/API key.
- The skill tree is populated with demo roadmap data.
- Micro-project creation/submission uses the local demo responses.
- Learner dashboard shows demo progress/verification data.
- Employer matching shows named demo learners with match percentages.
- Employer hiring requirements are pre-filled.
- Demo sign-in does not require a backend account.

Start:
  cd frontend
  npm run dev

Open:
  http://localhost:3000

The backend/database are not required for the demo flow.
