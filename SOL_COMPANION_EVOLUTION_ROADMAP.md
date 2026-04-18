# Sol Companion Evolution Roadmap

This roadmap defines the implemented and next-phase evolution path while preserving standalone app boundaries.

## Phase 1 (Implemented)
- Deeper reflection through mode-aware prompting.
- Better grounding with optional breath-based invitation.
- New UI modes: Companion, Presence, Insight, Journal.
- Journaling features with local journal memory entries.
- Presence mode (metaphorical, slow, deep cadence).
- Insight mode (pattern reflection without directive advice).
- Emotional thread detection using lightweight marker extraction.
- Session summaries with local memory persistence.
- Voice mode in UI using browser speech APIs.
- Mobile UI refinements for mode/action controls.

## Phase 2 (Near-term)
- Journaling timeline view with tag filters.
- Session summary history panel.
- Presence timer with optional chime-free pacing.
- Insight streak detection (recurring pattern signatures over sessions).

## Phase 3 (Advanced)
- Optional local TTS/ASR provider integration (offline models).
- Adaptive grounding style selection from emotional marker trends.
- Weekly reflective digest from session summaries.

## Boundary Guardrails
- Keep Sol Companion app code under /home/young/sol-companion.
- Reuse AIStudio runtime services via runtime bridge imports.
- Do not copy AIStudio manifests into Sol Companion.
