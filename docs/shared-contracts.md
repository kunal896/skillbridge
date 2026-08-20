# Shared Contracts — Team Agreement

## Why this exists

The team is using AI tools independently. Shared contracts are the "plug shape"
that keeps independently-built modules compatible.

## Ownership

- Anyone may propose a contract change.
- The person changing a contract must tell the team.
- Do not change contract fields just to fit an AI-generated implementation.
- Prefer adapting your implementation to the contract.

## Current module boundaries

### Diagnosis
Input:
- `LearnerProfile`

Output:
- `DiagnosisResult`

### RAG / Roadmap
Input:
- `DiagnosisResult`
- `JobPosting` retrieval results

Output:
- `RoadmapResult`

### Verification
Input:
- `MicroProject`
- learner submission

Output:
- `VerificationResult`

### Matching
Input:
- `LearnerProfile`
- verified skills from `VerificationResult`
- `EmployerRequirement`

Output:
- `MatchResult`

## Versioning

Contract changes must update the `version` field and be discussed in the PR.
Do not silently rename fields.

## Never commit secrets

API keys belong in `.env`, not in shared contracts, source code, README files,
or sample JSON.
