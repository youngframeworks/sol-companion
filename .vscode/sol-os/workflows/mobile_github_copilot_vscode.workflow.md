# Workflow: Mobile -> GitHub -> Copilot -> VS Code

## Purpose
Bootstrap task intake and execution from mobile capture into cloud orchestration and local engineering workspace.

## Sequence
1. Capture request on mobile and create GitHub Issue (`sol-task`).
2. SolManagerAgent loads issue context in Copilot Cloud.
3. Workflow and agent chain are selected.
4. Patch is generated and validated.
5. Local workspace receives updates and OS mirror state.

## Outputs
- Issue-to-patch traceability
- Reproducible local sync state
