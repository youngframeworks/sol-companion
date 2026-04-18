# Policy: Boundaries

## Boundary Matrix
- Cloud OS: orchestration contracts, policies, workflows, skills.
- Project runtime: source code, runtime configs, tests.
- Local validation runtime: AIStudio and local model simulations.

## Hard Constraints
- No runtime code in Cloud OS contract paths.
- No Cloud OS source-of-truth files in app runtime directories.
- Sync destination limited to `.vscode/sol-os/` for project mirrors.
