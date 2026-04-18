# Workflow: Auto Sync to GitHub

## Trigger
- `sol push ["commit message"]` from terminal
- GitHub Actions `sol-auto-sync.yml` on every merge to `main`
- Manual: `@SolManagerAgent push to github`

## Purpose
Ensure every tracked file change in the workspace is committed and pushed to the correct
GitHub repository as **individual files** — never as blobs, archives, or packed objects.

Cloud OS changes flow out → project mirrors are re-synced before each push.

## Inputs
- Current working directory (must be inside a git repository)
- `sol-os-cloud/OS_MANIFEST.md` (version source)
- `.vscode/sol-os/` (mirror health check)
- Optional: commit message string

## Sequence

1. **Pre-flight validation** (local)
   - Confirm inside a git repository.
   - Block binary model artifacts: `.gguf`, `.bin`, `.pkl`, `.pt`, `.pth`, `.safetensors`.
   - Run `bash sol-os-cloud/scripts/sync_os_to_project.sh --target all` to ensure mirrors are current.

2. **Stage** (`git add -A`)
   - Adds all tracked and new files, respecting `.gitignore`.
   - `.gitignore` must exclude: `logs/`, `pids/`, `models/gguf/`, `*.pid`, `*.log`.

3. **Commit**
   - If a message was supplied: use it verbatim.
   - If no message: auto-generate `chore: sol push <ISO8601_timestamp>`.
   - If nothing to commit: print notice and continue (non-fatal).

4. **Push** (`git push`)
   - Pushes to the configured remote (`origin`) on the current branch.
   - On failure: print the git error and exit non-zero.

5. **Confirm**
   - Print `✅ Push complete.` with remote and branch.
   - Log to terminal. No file modifications after this point.

## GitHub Actions integration

`sol-auto-sync.yml` runs automatically on every push to `main`.
It performs:
- OS boundary validation (no non-markdown in `sol-os-cloud/os/`)
- Mirror drift detection (source ↔ `.vscode/sol-os/` file count)
- Binary artifact rejection (model files blocked from push)
- Individual file sync validation report
- sol-companion OS mirror change detection (triggers companion update)
- Final sync summary with per-repo status

Companion workspace (`youngframeworks/sol-companion`) receives OS mirror changes
automatically when `sol-os-cloud/os/` files change in a push to `main`.

## Output

On `sol push`:
```
[sol] Syncing OS mirrors...
[sol]   [sync] completed successfully
[sol] Pushing to remote...
[sol] ✅ Push complete.
```

On `sol-auto-sync.yml`:
```
╔══════════════════════════════════════════════════════╗
║       Sol OS v3.1 — Auto Sync Summary                ║
╚══════════════════════════════════════════════════════╝
  Pre-sync validation : success
  aistudio sync       : success
  sol-companion sync  : success
  ✅ SYNC COMPLETE — all individual files live in GitHub.
```

## Constraints
- Binary model files (`.gguf`, `.bin`) are NEVER pushed. `.gitignore` enforces this.
- OS mirrors must be up to date before any push. `sol push` auto-syncs.
- Never force-push (`--force`) without explicit user confirmation.
- Never rebase or amend published commits via this workflow.
- Project changes never overwrite `sol-os-cloud/os/` (one-way sync enforced).
- Commit message must be non-empty; if none supplied, timestamp auto-message is used.

## Human-Gate Notes
`sol push` is an explicit user action (terminal command). It does NOT run automatically
from within Copilot Chat sessions. SolManagerAgent may propose a `sol push` call in its
output, but the user must run it manually.
