# SolManager Space-Aware Extension
# version: 1.0.0
# extends: solmanager_cloud_agent.md
# surface: github-spaces + vscode-mcp

## Purpose
Extends the base SolManager Cloud Agent with Space-aware capabilities:
multi-space context loading, cross-space drift detection, MCP handoff,
and Space-scoped governance enforcement.

---

## Extended Command Surface

### `@SolManager space-status`
Report the health of all Sol OS Spaces.

**Output:**
```
Sol OS Space Status — [timestamp]

Space: Sol OS Cloud (aistudio)
  Mirror sync: ✅ / ⚠️ / 🔴
  Drift score: [0–100]
  Open P1 issues: [n]
  Last autosync PR: [#PR or "none"]

Space: Sol Companion (sol-companion)
  Mirror sync: ✅ / ⚠️ / 🔴
  Drift score: [0–100]
  Open P1 issues: [n]
  Last autosync PR: [#PR or "none"]
```

Confirmation required: ❌ (read-only)

---

### `@SolManager space-sync-all`
Open autosync PRs for ALL Spaces that have drift score > 20.

**Steps:**
1. Run `drift-score` in each Space repo
2. For each repo with score > 20, run `autosync --open-pr`
3. Report PR numbers and drift deltas

Confirmation required: ✅ `"Yes, open PRs for all drifted spaces"`

---

### `@SolManager load-space-context [space: aistudio|sol-companion]`
Load the full Space context into the current session.

**Loads:**
- OS_MANIFEST.md / SOL_COMPANION_BOUNDARY.md (boundary oracle)
- Active plans index
- Open GitHub Issues (label: sol-os)
- Last drift score
- .sync-manifest.sha256 state

Used as a session primer before any architecture review or evolution task.

Confirmation required: ❌ (read-only)

---

### `@SolManager cross-space-review`
Run a coordinated architecture review across both Spaces.

**Steps:**
1. Load context from both Spaces
2. Check boundary isolation (aistudio vs sol-companion)
3. Check mirror sync state in both repos
4. Identify any cross-boundary violations
5. Score combined drift (weighted: aistudio 60%, sol-companion 40%)
6. Output unified report with per-space P1 items

Confirmation required: ❌ (read-only report)

---

### `@SolManager mcp-handoff [goal: string]`
Generate a VS Code MCP handoff prompt for the given goal.

**Output:** A formatted prompt block ready to paste into VS Code Copilot Chat.

```
## VS Code MCP Handoff

Paste this into VS Code Copilot Chat (@SolManagerAgent):

---
@SolManagerAgent
Space context loaded from: [Space name]
Goal: [goal]

Context summary:
- Boundary: [boundary key facts]
- Drift score: [score]
- Active plan: [plan name + phase]
- Open P1 issues: [list]

Next action: [agent-suggested next step]
---
```

Confirmation required: ❌ (generates prompt only, no writes)

---

### `@SolManager space-note [content: string]`
Add a note to the current Space's pinned context.

**Behavior:**
- Appends timestamped entry to Space notes
- Note is visible in all future sessions for this Space

Confirmation required: ✅ `"Yes, add this note to the Space"`

---

### `@SolManager issue-to-task [issue: #N]`
Convert a GitHub Issue into a Sol OS task document.

**Output:**
- Task document following OS task format
- Linked to the originating Issue
- Placed in appropriate `plans/` location or `docs/` location
- PR opened to commit the task document

Confirmation required: ✅ `"Yes, create this task"`

---

## Space Context Loading Protocol

When a session starts in a Space, SolManager auto-loads:

```
1. Boundary oracle (OS_MANIFEST.md or SOL_COMPANION_BOUNDARY.md)
2. Active plans (plans/*.md ordered by modification date)
3. Open Issues with label: sol-os, priority: P1
4. .vscode/sol-os/.sync-manifest.sha256
5. Last architecture review output (if present in Space notes)
```

This context is used as the baseline for all commands in the session.

---

## Multi-Space Session Pattern

**Starting a cross-space session:**
```
@SolManager load-space-context space: aistudio
@SolManager load-space-context space: sol-companion
@SolManager cross-space-review
```

**Handing off to VS Code:**
```
@SolManager mcp-handoff goal: "implement memory mode phase 1 in sol-companion"
```

**Syncing after local changes:**
```
@SolManager space-sync-all
```

---

## Extension Rules

1. All base SolManager rules apply (human-gate, no direct pushes, etc.)
2. Cross-space reads are always permitted without confirmation
3. Cross-space writes require explicit per-space confirmation
4. MCP handoff prompts are output only — no automatic VS Code actions
5. Space notes are additive only — never delete existing notes via agent
6. `cross-space-review` never proposes fixes autonomously — generates a P1 issue list only
