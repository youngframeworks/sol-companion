# Sol Companion Space Blueprint
# workflow: sol_companion_space_blueprint
# version: 1.0.0
# surface: github-spaces

## Purpose
Define the GitHub Copilot Space configuration for the `sol-companion` repository,
enabling SolManager Cloud Agent to use it as a governed OS surface with full
context awareness, PR/issue integration, and MCP handoff to VS Code.

---

## Space Identity

| Field        | Value                              |
|--------------|------------------------------------|
| Name         | Sol Companion — OS Surface         |
| Repos        | youngframeworks/sol-companion      |
| Agent        | @SolManager (Cloud Agent)          |
| Tier         | Companion Surface (Sol OS v3.2)    |
| Governance   | Human-gate required for writes     |

---

## Pinned Repositories

- `youngframeworks/sol-companion` — primary repo
- `youngframeworks/aistudio` — shared OS source-of-truth reference

---

## Pinned Agent

**@SolManager**

Instructions reference: `sol-os-cloud/os/agents/solmanager_cloud_agent.md`

Agent capabilities active in this Space:
- `review-project-architecture` — full architecture audit of sol-companion
- `self-heal` — detect and patch drift from OS contracts
- `autosync` — open PRs to sync OS mirror into sol-companion
- `drift-score` — score sol-companion against OS contracts
- `load-task` — intake GitHub Issues as Sol OS tasks

---

## Pinned Artifacts

| Artifact                                | Purpose                                      |
|-----------------------------------------|----------------------------------------------|
| `SOL_COMPANION_BOUNDARY.md`             | Boundary contract — what sol-companion owns  |
| `SOL_COMPANION_EVOLUTION_ROADMAP.md`    | Active evolution plan                        |
| `plans/FULL_EVOLUTION_PLAN.md`          | Full multi-phase delivery plan               |
| `plans/FULL_MEMORY_MODE_PLAN.md`        | Memory mode architecture                     |
| `plans/FULL_VOICE_MODE_PLAN.md`         | Voice mode architecture                      |
| `plans/FULL_PRESENCE_MODE_PLAN.md`      | Presence mode architecture                   |
| `plans/FULL_GEMINI_LIVE_INTEGRATION_PLAN.md` | Gemini Live integration plan            |
| `app/sol_agent.py`                      | Core agent implementation                    |
| `app/sol_server.py`                     | Server entrypoint                            |
| `app/sol_workflow.py`                   | Workflow definitions                         |
| `app/runtime_bridge.py`                 | Runtime bridge to aistudio ADK               |

---

## Persistent Context Blocks

### Block 1 — Boundary Contract
```
sol-companion is a companion UI/agent surface for Sol OS.
It owns: UI layer, voice mode, presence mode, memory mode, Gemini Live integration.
It does NOT own: ADK runtime, agent definitions, workflow orchestration (those live in aistudio).
All writes require human confirmation via SolManager governance gate.
```

### Block 2 — Active Plans Index
```
Evolution plans are in plans/. Each plan is a fully specified delivery document.
Active: FULL_EVOLUTION_PLAN.md (phases 1-5), FULL_MEMORY_MODE_PLAN.md (P0).
Blocked on: Gemini Live key provisioning (FULL_GEMINI_LIVE_INTEGRATION_PLAN.md).
```

### Block 3 — Runtime Bridge
```
sol-companion connects to aistudio ADK runtime via app/runtime_bridge.py.
Default endpoint: http://localhost:8000/adk/run
The bridge is the ONLY integration point — do not add direct agent calls.
```

### Block 4 — Sol OS Mirror
```
Sol OS contracts are mirrored into sol-companion at .vscode/sol-os/.
The mirror is synced by SolManager autosync workflow.
Never edit .vscode/sol-os/ directly — it is regenerated on each sync.
```

---

## Session Starters

```
@SolManager
Run a full architecture review of sol-companion. Score drift and list P1 self-heal items.
```

```
@SolManager
Review FULL_EVOLUTION_PLAN.md and identify the next unblocked delivery task.
```

```
@SolManager
Check sol-companion for any boundary violations against SOL_COMPANION_BOUNDARY.md.
```

```
@SolManager
Open an autosync PR to bring sol-companion's OS mirror up to date with aistudio.
```

```
@SolManager
Load the memory mode plan and generate the next implementation task as a GitHub Issue.
```

---

## Space Constraints

- All agent-initiated writes require confirmation: `"Yes, apply this to sol-companion"`
- Autosync PRs must include drift score and changed file list
- No direct model or GGUF references — all inference routes through aistudio runtime bridge
- Architecture reviews must reference `SOL_COMPANION_BOUNDARY.md` as the boundary oracle
- Evolution tasks must trace to a plan in `plans/`
