# Skill: Sync Mirroring

## Purpose
Mirror Cloud OS definitions into project-local `.vscode/sol-os/` deterministically.

## Procedure
1. Build canonical file list from `os/`.
2. Copy using path-preserving mirror.
3. Remove stale local mirror files not present in source.
4. Produce checksum and change summary.

## Safeguards
- Never mirror runtime code into OS paths.
- Never mirror secrets or credentials.
