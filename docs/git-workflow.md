# Git Workflow

## 1. Pull before starting

    git checkout main
    git pull origin main

## 2. Create a branch

Use one branch per feature/task:

    git checkout -b feature/diagnosis-agent

## 3. Work only in your owned area

Example:

    agents/

Avoid unrelated formatting changes elsewhere.

## 4. Commit small steps

Examples:

    feat: add diagnosis result schema
    feat: implement diagnosis agent
    test: add diagnosis agent tests
    fix: handle empty resume input

## 5. Push

    git push -u origin feature/diagnosis-agent

## 6. Pull Request

Open a PR into `main`.

The PR should say:
- what changed
- how to test it
- whether a shared contract changed

## 7. After merge

Delete the feature branch and start a fresh branch for the next task.

## Merge-conflict rule

If Git reports a conflict:
1. Do not randomly choose "ours" or "theirs".
2. Stop and inspect the conflicting lines.
3. Ask the owner of that file if unsure.
4. Resolve the conflict.
5. Test.
6. Commit the merge fix.

## Protected area

Treat `shared/contracts/` as a team-owned protected area.
Changes need agreement before merge.
