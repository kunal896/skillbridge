# agents/

Multi-agent core of **SkillBridge** (AGENTRIX 2026). Fully aligned with `shared/contracts/` JSON schemas.

## Owns
- Diagnosis (`diagnosis_agent.py`) — skill-gap classification from resume/MCQ
- Roadmap reasoning (`roadmap_agent.py`) — RAG-grounded, cited roadmap generation
- Verification orchestration (`verification_agent.py`) — micro-project generation + grading
- LangGraph workflow (`orchestrator.py`) — wires the three agents into one graph

## Consumes
- Learner/job data — `tools.py: fetch_learner_profile`, `fetch_job_postings`
- RAG retrieval — `tools.py: retrieve_relevant_postings` (Chroma / Pinecone)
- Judge0 verification — `tools.py: run_judge0_submission`

## Structure
```
agents/
├── __init__.py
├── config.py              # env-driven settings with dotenv support
├── state.py                # shared AgentState / RoadmapNode / VerificationResult schemas
├── tools.py                 # external I/O: learner/job data, RAG, Judge0 with fallbacks
├── diagnosis_agent.py       # Agent 1a
├── roadmap_agent.py         # Agent 1b
├── verification_agent.py    # Agent 2
├── orchestrator.py          # LangGraph StateGraph wiring
├── requirements.txt         # dependency specifications
├── .env.example            # environment variable placeholders
└── README.md                # documentation
```

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env   # fill in ANTHROPIC_API_KEY etc.
```

## Usage

### Run via CLI locally:
```bash
python -m agents.main --target-role "Data Analyst" --resume "Retail associate, 2 years, Excel reporting, SQL"
```

### Run programmatically in Python:
```python
from agents import run_pipeline

state = run_pipeline({
    "learner_id": "abc123",
    "resume_text": "Retail associate, 2 years, strong Excel, basic SQL...",
    "target_role": "Data Analyst",
})

print(state["roadmap"])
```

To advance a learner through verification, call `run_pipeline` again with `active_submission` set to their micro-project code once they submit it — the graph resumes from the `verify` node.

