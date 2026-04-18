# Full Memory Mode Plan

Status: Authoritative
Scope: Memory refinement, journaling, emotional thread, summaries
Execution model: ANALYZE -> PLAN -> PATCH -> REVIEW -> TEST -> SUMMARY

## 1. ANALYZE
- Inspect memory schema and stored state file compatibility.
- Evaluate emotional thread marker quality and false positives.
- Assess journaling persistence limits and sanitization behavior.
- Review session summary quality and storage constraints.

## 2. PLAN
Target memory features:
- Robust schema migration for old memory files.
- Refined emotional marker extraction and scoring.
- Journaling entries with structured tags.
- Session summaries with concise, non-directive format.
- Memory retention windows and pruning rules.

Planned files:
- app/sol_agent.py
- app/sol_workflow.py
- app/sol_server.py
- app/ui/index.html
- README and roadmap docs

## 3. PATCH
Patch groups:
- Memory schema versioning and migration helpers.
- Emotional thread detection refinement and marker confidence.
- Journal entry add/list/filter support.
- Session summary generation and history retrieval.

Safety constraints:
- Continue sanitizing personal identifiers.
- Keep local-only storage by default.
- Keep data structures backward-compatible.

## 4. REVIEW
Reviewer checks:
- Data minimization and sanitization policy alignment.
- Backward compatibility for existing memory files.
- Boundary-safe storage location and import safety.

## 5. TEST
Tester checks:
- Migration from old to new schemas.
- Journal save/read/reset lifecycle.
- Session summary generation under model available/unavailable states.
- Emotional thread marker stability for representative prompts.
- Reset endpoint fully clears session and memory state.

## 6. SUMMARY
Report:
- Memory model changes
- Migration results
- Retention/sanitization status
- Remaining quality gaps and next iteration

## Acceptance Criteria
- No crashes with prior memory files.
- Journaling and summaries available and stable.
- Emotional thread tracking improved without exposing internal state labels.
- Reset reliably clears all soft-memory surfaces.
