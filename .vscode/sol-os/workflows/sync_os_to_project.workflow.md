# Workflow: Sync OS To Project

## Trigger
`@SolManagerAgent sync os to project`

## Sequence
1. Pull latest cloud source.
2. Mirror `os/` into `.vscode/sol-os/`.
3. Remove stale mirror files.
4. Run boundary guard checks.
5. Publish sync report and checksum.

## Scripted Execution
- Aistudio target:
	- `bash sol-os-cloud/scripts/sync_os_to_project.sh --target aistudio`
- Sol Companion target:
	- `bash sol-os-cloud/scripts/sync_os_to_project.sh --target sol-companion`
- Both targets in one operation:
	- `bash sol-os-cloud/scripts/sync_os_to_project.sh --target all`
- Dry-run validation (no writes):
	- `bash sol-os-cloud/scripts/sync_os_to_project.sh --target all --check-only`
