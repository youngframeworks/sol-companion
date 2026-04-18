# Sol CLI — Command Specification

All commands route to SolManagerAgent via `copilot chat -m "@SolManagerAgent <command>"`.

## Cloud OS commands

### `sol prepare-cloud-os`
Inspect and evolve the `sol-os-cloud` scaffold.
Produces a multi-file patch with any missing or updated agents, skills, workflows, and policies.

### `sol sync-os`
Mirror Cloud OS (`sol-os-cloud/os/`) into the project under `.vscode/sol-os/`.
Equivalent to: `bash sol-os-cloud/scripts/sync_os_to_project.sh --target <project>`
Validates boundary policy and writes a checksum manifest.

## Task commands

### `sol load-task`
Fetch the most recent open GitHub Issue labeled `sol-task`.
Parses title, body, labels, and linked PRs. Selects the appropriate Cloud OS workflow.

### `sol execute`
Run the full workflow for the currently loaded task:
Architect → Planner → Implementer → QA → GitOps.
Outputs: plan, multi-file patch, tests, commit message, PR summary.

### `sol test-locally`
Invoke AIStudio/local multi-agent runtime to simulate or validate behaviour.
Output is advisory only — CI (GitHub Actions) remains the final authority.

## Utility commands

### `sol help`
Show available commands and current workspace status.

### `sol version`
Print Sol OS version from `OS_MANIFEST.md`.

## Output contract
Every `sol` command produces:
1. Plan
2. Detailed steps
3. Multi-file patch (where applicable)
4. Validation checks
5. Suggested commit message
6. Suggested PR title and summary (where relevant)

## Environment variables
| Variable | Purpose | Default |
|---|---|---|
| `SOL_TARGET` | Default sync target | auto-detected |
| `SOL_OS_PATH` | Override Cloud OS path | `sol-os-cloud/` |
