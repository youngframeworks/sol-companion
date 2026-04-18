# Workflow: review_project_architecture

## Trigger
- Chat: `@SolManagerAgent review project architecture`
- CLI: `sol review-project-architecture`
- GitHub Action: `architecture-check.yml` on PR

## Purpose
Perform a full structural audit of the active project against Cloud OS governance
and produce a structured findings + recommendations report. No files are modified.

## Responsible Agent
SolManagerAgent (coordinator) → no sub-agent delegation; structural inspection only.

## Inputs
- Active workspace root
- `sol-os-cloud/os/` (source of truth)
- `.vscode/sol-os/` (project mirror)
- All policies in `os/policies/`

## Sequence

1. **Scan workspace**
   - Root structure (max depth 3, exclude .git, .venv, __pycache__, node_modules)
   - `.vscode/sol-os/` mirror completeness vs `sol-os-cloud/os/`
   - `scripts/`, `llama.cpp/`, `models/gguf/`
   - `.devcontainer/`, `.github/workflows/`
   - `adk_app/` runtime layout

2. **Validate against policies**
   - `boundaries.policy.md` — OS and project paths must not cross-contaminate
   - `governance.policy.md` — operations must be atomic, traceable
   - `reproducibility.policy.md` — no runtime artifacts committed; stable structure
   - `sync_strategy.policy.md` — mirror must be current; source is cloud
   - `atomic_operations.policy.md` — no in-place overwrites without rollback points
   - `models.policy.md` — model selection rules enforced

3. **Detect drift**
   - Mirror files missing from `.vscode/sol-os/`
   - Extra files in mirror not in source
   - `.gitignore` coverage gaps
   - Outdated agent definitions (version mismatch)
   - Missing workflows
   - Stale or orphaned files at wrong paths
   - Scripts referencing wrong paths
   - Duplicate data (e.g. logs, pids, gguf copies)
   - Devcontainer misalignment with devcontainer spec

4. **Evaluate runtime**
   - `models/gguf/` health (canonical, no duplicates)
   - `llama.cpp/` script path correctness
   - All 4 servers wired in `llamacpp_start.sh`
   - `.devcontainer/setup.sh` completeness
   - GitHub Actions presence and correctness

5. **Produce structured report**
   - Summary
   - Findings (DRIFT-xx, BUG-xx, STALE-xx, REDUNDANT-xx codes)
   - Enhancement proposals with priority
   - Required OS sync actions
   - Optional improvements
   - **Drift score** (see below)

6. **Compute drift score** (0–100, lower = more in spec)

   Score is the sum of weighted penalties across three dimensions:

   | Dimension | Max penalty | Measured by |
   |---|---|---|
   | **Config drift** | 40 | Files in source not in mirror; stale checksums |
   | **Structure drift** | 35 | Empty dirs, files at wrong paths, missing required sections |
   | **Policy drift** | 25 | `.gitignore` gaps, broken Actions, model mis-registration |

   Each violation in a dimension contributes proportionally:
   - High severity = full weight of its category / (number of items in category)
   - Medium = half weight
   - Low = quarter weight

   Final score: sum of all weighted penalties, capped at 100.

   Interpretation:
   - `0–10` — Healthy. No action required.
   - `11–30` — Minor drift. Schedule cleanup.
   - `31–60` — Significant drift. Run `sol self-heal` before next feature work.
   - `61–100` — Critical drift. Block PR merge until resolved.

## Output Contract

```
## Architectural Review — <project> — <date>

### Summary
...

### Drift Score
**Total: <N>/100**
| Dimension | Score | Max | Key violations |
|---|---|---|---|
| Config drift | | 40 | |
| Structure drift | | 35 | |
| Policy drift | | 25 | |

**Interpretation:** <Healthy / Minor drift / Significant drift / Critical drift>

### Findings
| Code | Severity | Description | Policy |
|------|----------|-------------|--------|

### Enhancement Proposals
| ID | Priority | Enhancement |

### OS Sync Required?
[ ] Mirror up to date  /  [ ] Run: sol sync-os

### Validation Checks
...
```

## Constraints
- Read-only audit. No files modified.
- Never modify `sol-os-cloud/os/` during a project review.
- Never flag `.sync-manifest.sha256` as an unexpected file in the mirror.
- A drift score ≥ 61 must be surfaced as a blocking warning in the report and in CI.
