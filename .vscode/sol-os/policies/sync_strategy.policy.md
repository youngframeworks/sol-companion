# Policy: Sync Strategy

## Directionality
- Source-of-truth: Cloud OS repository
- Mirror target: project `.vscode/sol-os/`

## Method
1. Build source inventory and hash list.
2. Apply deterministic mirror copy.
3. Remove stale targets not in source.
4. Recompute hashes and publish diff.

## Safety
- Skip secrets and environment-specific credentials.
- Abort sync on boundary violations.
