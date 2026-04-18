# Workflow: CLI Execution

## Trigger
Any `sol <command>` invocation from a terminal.

## Purpose
Define how SolManagerAgent behaves when invoked via the Sol CLI, ensuring
identical output to VS Code Chat invocation.

## Sequence
1. Parse CLI command and arguments.
2. Validate active workspace contains `.vscode/sol-os/`.
3. Load Cloud OS contracts from `.vscode/sol-os/`.
4. Select appropriate workflow from `workflows/`.
5. Execute via Copilot Cloud models.
6. Output to stdout:
   - Plan
   - Multi-file patch
   - Validation checks
   - Commit message
   - PR description (if relevant)

## Invariants
- CLI execution must produce identical output to VS Code Chat execution.
- No silent file modifications.
- All changes must be atomic and reversible.
- Every change must be traceable to a GitHub Issue where possible.
