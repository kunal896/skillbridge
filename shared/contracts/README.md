# Shared Contracts

These files define the data exchanged between SkillBridge modules.

## Golden rule

If your module consumes a shared contract, do not silently change its fields.

The safe process is:

1. Propose the contract change.
2. Update the contract version/changelog.
3. Tell the team.
4. Update all affected modules.
5. Run integration tests.

## Contract families

- `learner_profile.json` — normalized learner information
- `diagnosis.json` — diagnosis output and skill gaps
- `job_posting.json` — normalized job-posting representation
- `roadmap.json` — cited, sequenced learning roadmap
- `micro_project.json` — verification project definition
- `verification.json` — grading result and unlock decision
- `employer_requirement.json` — employer skill requirements
- `match.json` — learner/employer match result
- `api_response.json` — common API envelope

The contracts intentionally describe the business data rather than implementation details.
