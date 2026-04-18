# Workflow Request Templates

These are runnable, copy/paste templates for standardized SolManager workflow execution.

Use pattern:
- `/run-workflow name=<workflow_name> request="<request text>"`

## 1) Full Evolution Workflow
Workflow name:
- `sol_companion_evolution`

Quick run:
```text
/run-workflow name=sol_companion_evolution request="auto enhance Sol Companion"
```

Standardized payload block:
```text
MODE: evolution
OBJECTIVE: Evolve Sol Companion safely as a standalone app with AIStudio as brain/engine.
SCOPE:
- deeper reflection
- grounding quality
- UI polish and mobile UX
- emotional thread detection
- session summaries
CONSTRAINTS:
- obey SOL_COMPANION_BOUNDARY.md
- no OS/project cross-contamination
- atomic, reversible patches
VALIDATION:
- syntax/import checks
- startup check
- endpoint smoke tests
OUTPUT:
- analysis
- plan
- patches
- review
- tests
- summary
```

Runnable command with block:
```text
/run-workflow name=sol_companion_evolution request="MODE: evolution
OBJECTIVE: Evolve Sol Companion safely as a standalone app with AIStudio as brain/engine.
SCOPE:
- deeper reflection
- grounding quality
- UI polish and mobile UX
- emotional thread detection
- session summaries
CONSTRAINTS:
- obey SOL_COMPANION_BOUNDARY.md
- no OS/project cross-contamination
- atomic, reversible patches
VALIDATION:
- syntax/import checks
- startup check
- endpoint smoke tests
OUTPUT:
- analysis
- plan
- patches
- review
- tests
- summary"
```

## 2) Full Build Workflow
Workflow name:
- `sol_companion_build`

Quick run:
```text
/run-workflow name=sol_companion_build request="initial build"
```

Standardized payload block:
```text
MODE: build
OBJECTIVE: Build/refresh Sol Companion baseline scaffold as standalone app.
SCOPE:
- app structure
- server endpoints
- workflow wiring
- runtime bridge integrity
- docs and scripts
CONSTRAINTS:
- keep Sol Companion isolated under /home/young/sol-companion
- import shared runtime only via bridge patterns
- no duplicate manifests
VALIDATION:
- syntax/import checks
- startup check
- endpoint smoke tests
OUTPUT:
- scope
- plan
- patches
- tests
```

Runnable command with block:
```text
/run-workflow name=sol_companion_build request="MODE: build
OBJECTIVE: Build/refresh Sol Companion baseline scaffold as standalone app.
SCOPE:
- app structure
- server endpoints
- workflow wiring
- runtime bridge integrity
- docs and scripts
CONSTRAINTS:
- keep Sol Companion isolated under /home/young/sol-companion
- import shared runtime only via bridge patterns
- no duplicate manifests
VALIDATION:
- syntax/import checks
- startup check
- endpoint smoke tests
OUTPUT:
- scope
- plan
- patches
- tests"
```

## 3) Full Voice Mode Workflow
Workflow name:
- `sol_companion_voice_mode_evolution`

Quick run:
```text
/run-workflow name=sol_companion_voice_mode_evolution request="Evolve Sol Companion with voice mode using Gemini Live API"
```

Standardized payload block:
```text
MODE: voice
OBJECTIVE: Add robust voice mode with optional Gemini Live integration and safe fallbacks.
SCOPE:
- voice capture UX
- speech playback UX
- optional live session adapter
- browser unsupported fallback
- local text fallback
CONSTRAINTS:
- feature-flag cloud integration
- never hardcode secrets
- no client-side secret leaks
VALIDATION:
- unsupported browser checks
- API timeout/failure checks
- non-voice regression checks
OUTPUT:
- analysis
- plan
- patches
- tests
```

Runnable command with block:
```text
/run-workflow name=sol_companion_voice_mode_evolution request="MODE: voice
OBJECTIVE: Add robust voice mode with optional Gemini Live integration and safe fallbacks.
SCOPE:
- voice capture UX
- speech playback UX
- optional live session adapter
- browser unsupported fallback
- local text fallback
CONSTRAINTS:
- feature-flag cloud integration
- never hardcode secrets
- no client-side secret leaks
VALIDATION:
- unsupported browser checks
- API timeout/failure checks
- non-voice regression checks
OUTPUT:
- analysis
- plan
- patches
- tests"
```

## 4) Full Memory Mode Workflow
Workflow name:
- `sol_companion_memory_evolution`

Quick run:
```text
/run-workflow name=sol_companion_memory_evolution request="Add journaling mode and memory refinement to Sol Companion"
```

Standardized payload block:
```text
MODE: memory
OBJECTIVE: Refine memory model with journaling, emotional thread quality, and summaries.
SCOPE:
- schema migration safety
- journaling persistence
- emotional marker refinement
- summary generation and retention
CONSTRAINTS:
- sanitize personal identifiers
- preserve backward compatibility
- local-first storage
VALIDATION:
- migration checks
- summary endpoint checks
- reset lifecycle checks
OUTPUT:
- analysis
- plan
- patches
- tests
```

Runnable command with block:
```text
/run-workflow name=sol_companion_memory_evolution request="MODE: memory
OBJECTIVE: Refine memory model with journaling, emotional thread quality, and summaries.
SCOPE:
- schema migration safety
- journaling persistence
- emotional marker refinement
- summary generation and retention
CONSTRAINTS:
- sanitize personal identifiers
- preserve backward compatibility
- local-first storage
VALIDATION:
- migration checks
- summary endpoint checks
- reset lifecycle checks
OUTPUT:
- analysis
- plan
- patches
- tests"
```

## 5) Full Presence Mode Workflow
Workflow name:
- `sol_companion_presence_mode`

Quick run:
```text
/run-workflow name=sol_companion_presence_mode request="Enhance Sol Companion presence mode with metaphorical slow deep grounding"
```

Standardized payload block:
```text
MODE: presence
OBJECTIVE: Improve presence mode for metaphorical, slow, deep reflection quality.
SCOPE:
- presence prompt quality
- breath-based grounding style
- pacing and mode UX hints
- mobile behavior consistency
CONSTRAINTS:
- non-directive tone
- safety under intensity/crisis inputs
- no regressions in other modes
VALIDATION:
- mode switch regression checks
- grounding quality checks
- mobile UI checks
OUTPUT:
- analysis
- plan
- patches
- tests
```

Runnable command with block:
```text
/run-workflow name=sol_companion_presence_mode request="MODE: presence
OBJECTIVE: Improve presence mode for metaphorical, slow, deep reflection quality.
SCOPE:
- presence prompt quality
- breath-based grounding style
- pacing and mode UX hints
- mobile behavior consistency
CONSTRAINTS:
- non-directive tone
- safety under intensity/crisis inputs
- no regressions in other modes
VALIDATION:
- mode switch regression checks
- grounding quality checks
- mobile UI checks
OUTPUT:
- analysis
- plan
- patches
- tests"
```

## Optional: Minimal One-Liners
```text
/run-workflow name=sol_companion_evolution request="auto enhance Sol Companion"
/run-workflow name=sol_companion_build request="initial build"
/run-workflow name=sol_companion_voice_mode_evolution request="voice mode with Gemini Live, with fallback"
/run-workflow name=sol_companion_memory_evolution request="journaling, memory refinement, session summaries"
/run-workflow name=sol_companion_presence_mode request="presence mode: metaphorical slow deep grounding"
```
