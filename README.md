# Sol Companion

Sol Companion is a separate local application that uses the AI Studio multi-agent OS runtime as its engine while keeping a clean project boundary.

## What Sol Companion Is

- A reflective inner-voice companion.
- Grounded in Spiral Dynamics, body awareness, and consciousness frameworks.
- Poetic, calm, non-directive, and local-first.

## Behavior Contract

- Sol silently classifies internal conversational tone as `REFLECTION`, `INTENSITY`, or `CRISIS`.
- Internal state labels are never shown to the user.
- Soft memory stores only themes, recent messages, and emotional thread excerpts.
- Soft memory now includes journal entries and session summaries.
- Soft memory does not preserve direct personal identifiers.
- `Reset Space` clears both server memory and UI chat state.

### Evolved Capabilities

- Deeper reflection with mode-aware prompts.
- Better grounding with optional breath-based grounding cues.
- New modes: `companion`, `presence`, `insight`, `journal`, `memory`, `voice`, `gemini_live`.
- Journaling features with local journal entry persistence.
- Presence mode (metaphorical, slow, deep pacing).
- Insight mode (pattern reflection).
- Emotional thread detection via lightweight markers.
- Session memory summaries.
- Voice mode in the mobile-friendly UI.

## Architecture Generated

```text
sol-companion/
  app/
    __init__.py
    runtime_bridge.py
    sol_agent.py
    sol_workflow.py
    sol_server.py
    ui/index.html
  scripts/run.sh
  README.md
```

### Runtime Integration

Sol Companion imports and reuses the following runtime components from `aistudio/adk_app`:

- `session_service` (shared session infrastructure)
- model `registry` / llama.cpp backend
- `Logger`
- runtime path bootstrap
- OS governance path summary (`os_root_summary`)

`runtime_bridge.py` performs the integration and keeps the app boundary clean by importing from the sibling project instead of copying logic.

## Workflow

```text
User -> SolCompanionAgent -> Response
```

No routing, no planner, no branching.

## API Endpoints

- `GET /` serves the minimalist zen UI.
- `POST /sol` sends a message to Sol.
- `POST /sol/reset` clears memory and session thread.
- `POST /sol/summary` generates and stores a session summary.
- `GET /sol/modes` returns available UI/backend interaction modes.
- `GET /sol/evolution/status` returns v3.2 Phase 1 track states.
- `GET /sol/next-task` returns current top-priority evolution task.
- `POST /sol/evolution/start` updates a specific track state.
- `GET /sol/dependency-graph` returns Mermaid graph for Space dashboards.

## Run Locally

```bash
cd /home/young/sol-companion
chmod +x scripts/run.sh
./scripts/run.sh
```

Then open:

- `http://127.0.0.1:8777/`

## Example Calls

```bash
curl -s http://127.0.0.1:8777/sol \
  -H 'Content-Type: application/json' \
  -d '{"message":"I feel scattered and tired","session_id":"sol-default"}'

curl -s http://127.0.0.1:8777/sol/reset \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"sol-default"}'
```

## OS and Project Separation

- Sol Companion remains fully contained under `sol-companion/`.
- Shared runtime services are imported from `aistudio/adk_app` through `runtime_bridge.py`.
- No AI Studio manifests are duplicated in this project.
- Governance references are read-only via OS root resolution.

See the explicit boundary contract:

- `SOL_COMPANION_BOUNDARY.md`

## Build With SolManagerAgent

Copilot OS prompt files:

- `/home/young/.copilot/os/prompts/sol-manager-companion.prompt.md`
- `/home/young/.copilot/os/prompts/sol_manager_companion.md`

Quick command available in OS quick commands:

- `Build Sol Companion`
- `Evolve Sol Companion`

Workflow-oriented quick commands:

- `Run Sol Companion Evolution Workflow`
- `Run Sol Companion Build Workflow`
- `Run Sol Companion Voice Workflow`
- `Run Sol Companion Memory Workflow`
- `Run Sol Companion Presence Workflow`

This keeps Sol Companion as a separate app while using AIStudio as the runtime engine.

## Evolution Roadmap

- `SOL_COMPANION_EVOLUTION_ROADMAP.md`

## Authoritative Plan Set

- `plans/README.md`
- `plans/FULL_EVOLUTION_PLAN.md`
- `plans/FULL_VOICE_MODE_PLAN.md`
- `plans/FULL_MEMORY_MODE_PLAN.md`
- `plans/FULL_PRESENCE_MODE_PLAN.md`
- `plans/FULL_GEMINI_LIVE_INTEGRATION_PLAN.md`
- `plans/WORKFLOW_REQUEST_TEMPLATES.md`

## SolManager Workflow Suite

Generated under AIStudio workflows:

- `aistudio/workflows/sol_companion_evolution_workflow.py`
- `aistudio/workflows/sol_companion_build_workflow.py`
- `aistudio/workflows/sol_companion_voice_mode_evolution_workflow.py`
- `aistudio/workflows/sol_companion_memory_evolution_workflow.py`
- `aistudio/workflows/sol_companion_presence_mode_workflow.py`

These workflows enforce deterministic stages:

1. Analyze
2. Plan
3. Generate patches
4. Validate boundaries
5. Test
6. Summarize
