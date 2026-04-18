# Sol Companion Boundary Contract

This file defines the separation contract for building Sol Companion with SolManagerAgent.

## App Identity
- Sol Companion is a standalone app rooted at /home/young/sol-companion.
- It owns its own server, workflow, UI, scripts, and local state.
- AIStudio is the brain and engine that powers Sol Companion generation and evolution.
- Sol Companion is enhanced continuously, but remains standalone at the app boundary.

## Allowed Dependency Direction
- sol-companion -> aistudio/adk_app (imports only)
- sol-companion -> ~/.copilot/os (read-only governance context)

## Forbidden Dependency Direction
- aistudio must not import sol-companion internals.
- sol-companion must not copy or fork AIStudio manifest/governance files.
- OS layer must not be modified by Sol Companion runtime code.

## Required Runtime Pattern
- Keep runtime bridging in app/runtime_bridge.py.
- Reuse AIStudio services via imports, not code duplication.
- Keep all Sol Companion behavior files under app/.

## Build Rule for SolManagerAgent
When executing "Build Sol Companion":
1. Modify files under /home/young/sol-companion first.
2. Touch /home/young/aistudio only when integration shims are strictly necessary.
3. Validate: syntax, imports, startup, endpoint smoke tests.
4. Report residual risks (for example: model endpoint unavailable).

When executing "Evolve Sol Companion" or "Auto enhance Sol Companion":
1. Use AIStudio runtime capabilities as the intelligence/engine layer.
2. Keep all product-facing Sol Companion changes in /home/young/sol-companion.
3. Reject any change that collapses Sol Companion into AIStudio internals.
4. Ship only reversible, validated enhancements.
