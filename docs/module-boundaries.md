# Module Boundaries

## frontend/
Owns:
- pages
- components
- frontend API client
- UI state
- skill-tree rendering

Consumes:
- backend API contracts

## backend/
Owns:
- HTTP API
- auth
- persistence
- service orchestration
- progress ledger

Consumes:
- shared contracts
- agent/RAG services

## agents/
Owns:
- diagnosis
- roadmap reasoning
- verification orchestration
- LangGraph workflow

Consumes:
- learner/job data
- RAG retrieval
- Judge0 verification

## rag/
Owns:
- job ingestion
- normalization
- embeddings
- retrieval
- citation metadata

## matching/
Owns:
- feature construction
- learner/employer scoring
- match explanation

## shared/
Owns:
- stable data contracts
- enums
- system-wide constants

## Safe editing rule

If your task can be completed without changing another module, do not edit it.
If you must edit another module, tell its owner and do it in the same PR.
