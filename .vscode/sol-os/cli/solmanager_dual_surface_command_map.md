# SolManager Dual-Surface Command Map

## Purpose
Map local VS Code commands to Cloud Agent commands so handoff is deterministic.

## Surfaces
- Local surface: `@SolManagerAgent` (workspace files, CLI, local context)
- Cloud surface: `@SolManager` (GitHub repos, PRs, cloud workflows)

## Command Map

| Intent | Local command | Cloud command | Expected outcome |
|---|---|---|---|
| Architecture review | `@SolManagerAgent review project architecture` | `@SolManager Run a full architecture review on <project>.` | Drift score + findings |
| Self-heal proposal | `@SolManagerAgent self heal` | `@SolManager Propose self-heal for <project>.` | Proposed changes only |
| Self-evolve proposal | `@SolManagerAgent self evolve` | `@SolManager Propose vNext evolution cycle.` | Versioned evolution plan |
| Autosync | `sol autosync` or `@SolManagerAgent autosync` | `@SolManager Run autosync for current Cloud OS changes.` | PR branch/title/body plan |
| Apply autosync | `sol autosync --open-pr` | `@SolManager Apply autosync.` | PR opened, no auto-merge |
| Docs-only drift cleanup | `@SolManagerAgent self heal` (selective) | `@SolManager Apply P1 self-heal only. Do not modify .vscode/sol-os.` | P1 docs drift reduced |
| Governance recheck | `sol review-project-architecture` | `@SolManager Re-run architecture review.` | Updated drift score |

## Handoff Pattern

1. Local analysis
- `@SolManagerAgent Review local workspace and mirror readiness.`

2. Cloud continuation
- `@SolManager Continue this analysis on the GitHub repo.`

3. Apply gate
- `Apply autosync`
- `Apply self-heal`
- `Apply evolution`

## Constraints
- Cloud and local analyses should use the same workflow contracts.
- Apply phrases are required before write operations.
- Autosync must only modify `.vscode/sol-os/*` in target repos.
- Never force-push and never auto-merge.
