# SkillBridge Matching Module

This module owns employer ↔ learner matching. It is intentionally independent
of the FastAPI implementation so it can be developed by the ML/matching owner
without editing `backend/`.

## Inputs

- shared learner profile data
- verified skills produced by the verification flow
- shared employer requirements

## Output

A `shared.types.types.MatchResult`, which maps directly to the backend's
`/api/v1/matches` request shape.

## Scoring

The MVP model is deterministic and explainable:

- skill presence and level contribute 60%
- verified competence contributes 40%
- employer skill weights change each skill's contribution

This is a stable baseline for the hackathon. The `SkillMatchModel` boundary can
later be replaced with a trained classifier without changing the service or
backend contract.

## Run tests

From the repository root:

    pytest matching/tests

## Boundary rule

Do not edit `backend/` from this module. Send a computed `MatchResult` to the
backend integration layer instead.
