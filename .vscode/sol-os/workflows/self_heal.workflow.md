# Workflow: self_heal

## Trigger
- Chat: `@SolManagerAgent self heal`
- CLI: `sol self-heal`

## Purpose
Detect drift between Cloud OS and project mirrors, broken paths, stale files,
and misconfigured scripts. Propose a minimal atomic patch. Apply only after
explicit user confirmation. Never self-apply.

## Responsible Agent
SolManagerAgent → BoundaryGuardSkill → ImplementerAgent (patch generation only)

## Inputs
- Active workspace root
- `sol-os-cloud/os/` source
- `.vscode/sol-os/` mirror
- `.gitignore`
- Script files under `scripts/`, `llama.cpp/`, `sol-os-cloud/scripts/`

## Sequence

1. **Detect** (read-only pass)
   Run equivalent of `review_project_architecture` silently.
   Categorise issues:
   - `DRIFT` — mirror vs source mismatch
   - `PATH` — script references broken paths
   - `STALE` — orphaned files, empty dirs, superseded scripts
   - `CONFIG` — .gitignore gaps, devcontainer errors, broken Actions

2. **Score** severity
   - 🔴 High — blocking correctness or security
   - 🟡 Medium — technical debt, reliability risk
   - 🟢 Low — ergonomic improvement

3. **Propose patch**
   - Present ALL proposed changes before touching anything.
   - Group into atomic units: each unit has a single intent and can be reverted alone.
   - Output format:

```
## Self-Heal Proposal — <timestamp>

### Detected Issues
| Code | Severity | File/Path | Description |

### Proposed Changes
#### Change 1: <intent>
- File: <path>
- Action: <create|modify|delete>
- Reason: <policy reference>

...

### ⚠️ Human gate — NO changes are applied until you confirm.
Reply: "Apply self-heal" (all) or "Apply change 1, 3" (selective)
Deletions ALWAYS require separate confirmation even if other changes are approved.
```

4. **Apply** (only after confirmation)
   - Apply each confirmed change atomically.
   - Log each applied change with file, action, timestamp.

5. **Re-sync** (if mirror drift was fixed)
   Run: `bash sol-os-cloud/scripts/sync_os_to_project.sh --target all`

6. **Validate**
   Run: `bash scripts/verify_workspace_integrity.sh`
   Report pass/fail count.

## Output Contract
Always present proposal before applying. Never skip confirmation step.

## Constraints
- **Never auto-apply.** Patches must NOT be generated or applied until the user replies
  with "Apply self-heal" or "Apply change N" (exact phrase required).
- Deletions require separate explicit confirmation even if other changes are approved.
- Treat `.vscode/sol-os/` as read-only (sync-managed).
- Do not modify `sol-os-cloud/os/` files during self-heal of a project.
- Each change must have a policy reference; changes without a policy basis are rejected.
