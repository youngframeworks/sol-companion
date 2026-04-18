# Workflow: CLI Sync (Cloud OS → Project)

## Trigger
`sol sync-os` or `bash sol-os-cloud/scripts/sync_os_to_project.sh --target <selector>`

## Purpose
Mirror Cloud OS contracts into project workspace deterministically via terminal.

## Sequence
1. Identify Cloud OS source (`sol-os-cloud/os/`).
2. Identify target workspace(s): `aistudio`, `sol-companion`, or `all`.
3. Validate source boundary: contracts-only (`.md` files).
4. Mirror subtrees:
   - `agents/`
   - `skills/`
   - `workflows/`
   - `policies/`
   - `cli/`
5. Write mirror to `.vscode/sol-os/` in each target.
6. Remove stale files not present in source.
7. Write `.sync-manifest.sha256` checksum.
8. Output: synced files, removed files, checksum.

## Safety rules
- Never overwrite project-specific files outside `.vscode/sol-os/`.
- Abort on boundary violation (non-markdown in source).
- OS files are read-only by convention in target projects.
- Never sync secrets or credentials.
