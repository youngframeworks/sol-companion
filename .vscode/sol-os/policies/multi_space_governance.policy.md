# Sol OS Multi-Space Governance Profile
# version: 1.0.0
# scope: all-spaces
# surface: github-spaces + vscode-mcp

## Overview
This profile defines governance rules, ownership boundaries, sync contracts,
and agent authority across all Sol OS GitHub Spaces.

Sol OS v3.2 operates as a **distributed multi-space OS** spanning:

| Space            | Repo                              | Tier          | Primary Surface      |
|------------------|-----------------------------------|---------------|----------------------|
| Sol OS Cloud     | youngframeworks/aistudio          | OS Core       | Cloud Agent + MCP    |
| Sol Companion    | youngframeworks/sol-companion     | OS Surface    | Cloud Agent + MCP    |

---

## Source of Truth Hierarchy

```
sol-os-cloud/os/          ← CANONICAL — never edited by agents directly
    ├── agents/           ← agent contracts
    ├── cli/              ← CLI command map
    ├── policies/         ← governance policies
    ├── skills/           ← reusable skill definitions
    └── workflows/        ← workflow contracts (including this profile)

.vscode/sol-os/           ← MIRROR of sol-os-cloud/os/ in each repo
    (aistudio, sol-companion)
```

**Rule:** All changes flow canonical → mirror via autosync PRs. Never edit mirrors directly.

---

## Space Authority Matrix

| Action                        | @SolManager (Cloud) | @SolManagerAgent (Local) | Human Required |
|-------------------------------|---------------------|--------------------------|----------------|
| Read any Space context        | ✅ auto             | ✅ auto                  | ❌             |
| Run architecture review       | ✅ auto             | ✅ auto                  | ❌             |
| Generate drift score          | ✅ auto             | ✅ auto                  | ❌             |
| Open autosync PR              | ✅ auto             | ✅ auto                  | ✅ confirm PR  |
| Merge autosync PR             | ❌ never            | ❌ never                 | ✅ required    |
| Edit canonical OS contracts   | ❌ never            | ❌ never                 | ✅ required    |
| Edit mirror (.vscode/sol-os/) | ❌ never (read-only)| ❌ never (read-only)     | ❌ (autosync only)|
| Create GitHub Issues          | ✅ auto             | ✅ auto                  | ❌             |
| Push to main branch           | ❌ never            | ❌ never                 | ✅ required    |
| Deploy / run scripts          | ❌ never            | ❌ never                 | ✅ required    |

---

## Cross-Space Sync Rules

### Rule 1 — Canonical Propagation
When `sol-os-cloud/os/` in `aistudio` is updated:
1. SolManager detects drift via `drift-score` command
2. Autosync PR is opened in each target repo (aistudio mirror, sol-companion mirror)
3. Human reviews and merges each PR
4. Drift score is re-run to confirm ≤ 20

### Rule 2 — No Cross-Space Writes
An agent operating in Space A may not write to Space B.
Cross-space operations require a human to switch Spaces and confirm separately.

### Rule 3 — Mirror Integrity
`.vscode/sol-os/.sync-manifest.sha256` must match the sha256 of the canonical OS tree.
A mismatch triggers a P1 self-heal alert in the next architecture review.

### Rule 4 — Boundary Isolation
- `aistudio` owns: ADK runtime, agents, workflows, orchestration, model servers
- `sol-companion` owns: UI, voice, presence, memory, Gemini Live integration
- Neither may claim ownership of the other's boundary items
- Cross-boundary calls must go through `runtime_bridge.py` only

---

## Drift Score Thresholds

| Score   | State      | Action Required                              |
|---------|------------|----------------------------------------------|
| 0–20    | ✅ Healthy | No action                                    |
| 21–40   | ⚠️ Drift   | Schedule self-heal within 48h                |
| 41–70   | 🔴 Alert   | P1 self-heal before next feature work        |
| 71–100  | 🚨 Critical| Freeze feature work, immediate remediation   |

---

## Governance Confirmation Phrases

All agent-proposed writes must be confirmed with one of:

- `"Yes, apply this to aistudio"`
- `"Yes, apply this to sol-companion"`
- `"Yes, open the PR"`
- `"Yes, apply this change"`

Phrases that do NOT constitute confirmation:
- "looks good", "sure", "go ahead" (ambiguous)
- "yes" alone without context (ambiguous)

---

## MCP Integration Points

When VS Code MCP is connected to a Space, the following context is auto-loaded:

| Context Key               | Source                                      |
|---------------------------|---------------------------------------------|
| `os.boundaries`           | `SOL_COMPANION_BOUNDARY.md` / `OS_MANIFEST.md` |
| `os.active_plans`         | `plans/*.md` / `sol-os-cloud/SOL_OS_V3_2_ROADMAP.md` |
| `os.drift_state`          | Last drift-score output                     |
| `os.sync_manifest`        | `.vscode/sol-os/.sync-manifest.sha256`      |
| `os.open_issues`          | GitHub Issues (label: `sol-os`)             |

---

## Escalation Path

```
Agent detects issue
  → Creates GitHub Issue with label: sol-os, priority: P1
  → Adds to Space notes / dashboard
  → Human reviews in Space or VS Code MCP
  → Human confirms fix or delegates back to agent
```

No auto-merges. No silent writes. Every mutation is traceable.
