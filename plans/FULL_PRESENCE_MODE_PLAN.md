# Full Presence Mode Plan

Status: Authoritative
Scope: Presence mode (metaphorical, slow, deep)
Execution model: ANALYZE -> PLAN -> PATCH -> REVIEW -> TEST -> SUMMARY

## 1. ANALYZE
- Inspect current presence mode behavior in prompts and UI.
- Measure response pacing, tone consistency, and grounding quality.
- Identify where presence mode diverges from intended reflective style.

## 2. PLAN
Presence mode goals:
- Metaphorical and spacious language.
- Slow cadence and concise pacing.
- Gentle breath-oriented grounding options.
- No directive coaching style.

Planned changes:
- Prompt shaping in app/sol_agent.py.
- UI pacing hints and mode guidance in app/ui/index.html.
- Optional timed presence prompts without intrusive notifications.

## 3. PATCH
Patch groups:
- Presence-specific prompt policy block.
- UI mode hints and controls for presence depth.
- Grounding phrase library with subtle variation.
- Session summary tags to reflect presence-mode sessions.

Reversibility:
- Presence behavior isolated behind mode switch.
- Existing companion/insight/journal behavior unchanged.

## 4. REVIEW
Reviewer checks:
- Tone aligns with non-directive, grounding principles.
- No safety regressions under intensity/crisis inputs.
- Boundary-safe and deterministic patch set.

## 5. TEST
Tester checks:
- Presence mode response quality for calm and intense prompts.
- Breath grounding insertion behavior when enabled.
- Mode switching regressions across all modes.
- Mobile usability of presence controls.

## 6. SUMMARY
Report:
- Presence mode quality improvements
- Safety outcomes
- UX outcomes on mobile and desktop
- Next refinements

## Acceptance Criteria
- Presence mode reliably produces slow, deep, metaphorical reflections.
- Grounding support feels natural and optional.
- No regression in other modes or endpoints.
