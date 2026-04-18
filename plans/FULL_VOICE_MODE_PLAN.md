# Full Voice Mode Plan

Status: Authoritative
Scope: Voice input/output evolution for Sol Companion
Execution model: ANALYZE -> PLAN -> PATCH -> REVIEW -> TEST -> SUMMARY

## 1. ANALYZE
- Inspect current browser voice mode implementation in UI.
- Verify current API contract for /sol payload supports mode and grounding flags.
- Identify gaps for live streaming voice sessions and fallback behavior.
- Assess privacy constraints and local-first behavior.

## 2. PLAN
Target capabilities:
- Stable voice capture UX with explicit start/stop.
- Safe TTS playback controls.
- Graceful fallback when speech APIs are unsupported.
- Optional Gemini Live mode behind explicit feature flag.

Planned files:
- app/ui/index.html
- app/sol_server.py
- app/sol_workflow.py
- app/live_client.py (optional integration adapter)
- README updates

## 3. PATCH
Patch groups:
- UI controls and state machine for voice sessions.
- Backend support for live voice session endpoint if enabled.
- Integration adapter for Gemini Live API with timeout and fallback.
- Feature-flag gated path to avoid hard dependency failures.

Reversibility:
- Feature flag defaults to off.
- Adapter isolated in dedicated file.
- Existing text chat path remains primary and unaffected.

## 4. REVIEW
Reviewer checks:
- Boundary safety and standalone integrity.
- No forced cloud dependency.
- No credential leakage in client code.
- Fallback behavior exists for API/network errors.

## 5. TEST
Tester checks:
- Browser API support and unsupported-browser fallback.
- Voice start, stop, and recovery behavior.
- TTS playback behavior and interruption handling.
- Optional live endpoint handshake and timeout handling.
- Regression tests for standard non-voice chat.

## 6. SUMMARY
Report:
- Delivered voice capabilities
- Flag status and runtime requirements
- Risk notes (network, browser support, API limits)
- Next improvements

## Acceptance Criteria
- Voice mode works with browser APIs.
- No regression for text mode.
- Gemini Live path optional and safely disabled by default.
- Failure scenarios handled without app crash.
