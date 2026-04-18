# Skill: Boundary Guard

## Purpose
Prevent cross-contamination between Cloud OS metadata and project runtime code.

## Checks
- Cloud OS paths contain contracts, not runtime modules.
- Project runtime paths do not hold Cloud OS policy sources.
- Sync target is limited to `.vscode/sol-os/`.

## Result
- Pass/fail boundary status
- Violations with file paths and remediation
