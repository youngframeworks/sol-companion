# Workflow: AutoSync — Cloud OS → Project Mirrors → GitHub PRs

## Trigger
- Push to `main` touching `sol-os-cloud/**`
- Issue comment: `/autosync`
- `workflow_dispatch` (manual, supports dry-run flag)
- Scheduled: nightly at 02:00 UTC (opens PR only when drift exists)
- CLI: `sol autosync` (local detection + optional PR creation via `gh`)
- Chat: `@SolManagerAgent autosync`

## Purpose
Keep every project's `.vscode/sol-os/` mirror in sync with `sol-os-cloud/os/`
without any manual effort.

Cloud OS is the source of truth. When it changes, every downstream project must reflect
those changes. This workflow makes that propagation automatic, auditable, and governed.

## Inputs
- `sol-os-cloud/os/` — Cloud OS source (all markdown contracts)
- `sol-os-cloud/OS_MANIFEST.md` — current OS version
- `.vscode/sol-os/` — local mirror (target)
- `.vscode/sol-os/.sync-manifest.sha256` — checksum manifest for drift detection
- GitHub token (for PR creation)

## Sequence

1. **Validate Cloud OS** (always first)
   - Confirm OS boundary: no non-markdown files in `sol-os-cloud/os/`
   - Confirm all required directories exist: `agents`, `cli`, `skills`, `workflows`, `policies`
   - Read current OS version from `OS_MANIFEST.md`
   - If validation fails → abort. Never sync a broken Cloud OS.

2. **Detect drift** (read-only)
   - Compare `sol-os-cloud/os/` file set against `.vscode/sol-os/` file set
   - Compare checksums where manifest exists
   - Report: files added, files removed, files modified, total drift count
   - If no drift → skip PR creation (nightly + push triggers)
   - Manual triggers always proceed regardless of drift

3. **Apply mirror sync** (write, bounded)
   - Scope: ONLY `.vscode/sol-os/` — nothing outside this directory
   - Method: `rsync --delete` from `sol-os-cloud/os/` into `.vscode/sol-os/`
   - Regenerate `.sync-manifest.sha256` after sync
   - Verify: `git diff --name-only` must only contain `.vscode/sol-os/**` paths
   - If any path outside `.vscode/sol-os/` appears in diff → abort with error

4. **Commit**
   - Stage: `git add .vscode/sol-os/`
   - Message format:
     ```
     chore(sol-os-sync): update project OS mirror from Cloud OS vX.Y.Z

     AutoSync: Cloud OS vX.Y.Z → <project> mirror
     Trigger: <push|workflow_dispatch|issue_comment|schedule>
     Commit: <sha>
     ```
   - If nothing changed → print notice, skip commit, no PR

5. **Push autosync branch**
   - Branch name: `autosync/sol-os-<version>-<timestamp>`
   - Push to origin (never force-push)

6. **Open pull request**
   - Title: `[autosync] Update Sol OS mirror to vX.Y.Z`
   - Body: from `.github/pull_request_template_autosync.md` (populated with actuals)
   - Labels: `autosync`, `sol-os`
   - Base: `main`
   - Auto-merge: NEVER. Always requires human review.

## PR Body Contract

The PR must include:

```markdown
## AutoSync — Sol OS Mirror Update

**OS version:** `<version>`
**Files updated:** <count>
**Trigger:** <event>

### Files Updated
<list of changed files relative to .vscode/sol-os/>

### Safety Checks
- [ ] Only `.vscode/sol-os/` files modified
- [ ] OS boundary validated
- [ ] Checksum manifest regenerated
- [ ] No force-push used

### ⚠️ Human Gate
Do not merge until you have reviewed the diff.
```

## Constraints
- **Only `.vscode/sol-os/` is writable.** Any diff touching other paths aborts the sync.
- **Never auto-merge.** PR always requires human review and explicit merge.
- **Never force-push.** AutoSync branches are ephemeral but clean.
- **Never delete project-specific files** outside the OS mirror.
- **Never modify `sol-os-cloud/os/`** during a project sync — Cloud OS is read-only input.
- Sync must be idempotent — running twice with the same source produces the same result.
- If Cloud OS boundary is violated → entire autosync aborts. Fix the boundary first.
- Dry-run mode (`--check-only` / `dry_run: true`) must produce a report without writing files.

## Human-Gate Rule
AutoSync PRs are **always** reviewed before merge. SolManagerAgent proposes the PR;
the human merges. No exceptions.

The confirmation flow for `sol autosync` CLI:
- `sol autosync` → show drift report
- `sol autosync --open-pr` → detect + open PR via `gh`
- To apply locally without a PR: `bash sol-os-cloud/scripts/sync_os_to_project.sh --target all`

## Error States

| Error | Action |
|---|---|
| OS boundary violation | Abort. Print violations. Do not sync. |
| Required OS dir missing | Abort. Print missing dir. Do not sync. |
| Diff contains paths outside `.vscode/sol-os/` | Abort. Print violations. Revert branch. |
| `gh` CLI not available for PR creation | Print instructions. Exit 0 (non-fatal). |
| No drift detected (scheduled/push) | Skip PR. Print "Mirror current." |
