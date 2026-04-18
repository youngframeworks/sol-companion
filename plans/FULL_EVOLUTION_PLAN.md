# Full Evolution Plan

Status: Authoritative
Scope: Sol Companion standalone app, AIStudio-powered evolution
Execution model: Deterministic workflow stages

## 1. ANALYZE
- Inspect /home/young/sol-companion for missing or stale files.
- Compare current state with SOL_COMPANION_BOUNDARY.md and README contracts.
- Verify AIStudio runtime imports remain bridge-only.
- Verify workflow registrations and quick commands are present.
- Detect drift across modes, journaling, memory, summaries, voice, and mobile UI.

Output:
- State report: existing, missing, stale, drifted components.
- Risk report: boundary, dependency, runtime, migration risks.

## 2. PLAN
- Produce file-level plan with ordered, atomic steps.
- Prioritize safety-critical and boundary-critical fixes first.
- Include compatibility migrations for persisted state changes.
- Include rollout order: backend -> workflow -> API -> UI -> docs.

Planned areas:
- Reflection quality and grounding quality.
- Mode consistency across backend and UI.
- Emotional thread and session summary coherence.
- Voice mode reliability and fallback behavior.
- Mobile UX quality and responsiveness.

## 3. PATCH
- Generate deterministic, reversible patches.
- Patch set types:
  - Create files
  - Modify files
  - Remove obsolete files only when safe
- Include explicit rollback notes for each patch group.

Patch constraints:
- No OS layer writes from runtime code.
- No manifest duplication into Sol Companion.
- No leakage of Sol Companion internals into AIStudio app internals.

## 4. REVIEW
Reviewer checks:
- Boundary safety vs SOL_COMPANION_BOUNDARY.md.
- Standalone app integrity.
- Runtime bridge import safety.
- No cross-contamination between OS, AIStudio, and Sol Companion.
- No hidden dependency on unavailable cloud APIs.

Gate:
- safe to apply
- unsafe with blocking issues list

## 5. TEST
Tester dry-run and runtime checks:
- Syntax and import checks.
- FastAPI startup.
- Endpoint smoke tests:
  - GET /
  - POST /sol
  - POST /sol/reset
  - POST /sol/summary
  - GET /sol/modes
- UI behavior checks including mobile layout and mode switching.
- State migration and reset behavior checks.

Result:
- all tests passed
- failure report with exact repro steps

## 6. SUMMARY
Return final report sections:
- Analysis summary
- Plan summary
- Patch summary
- Review outcome
- Test outcome
- Final status and next actions

## Determinism Rules
- Stable stage order and stable output structure.
- No implicit side effects outside declared patch targets.
- Reversible changes by design.
- Clear acceptance criteria per stage.
