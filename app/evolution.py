"""Evolution track state for Sol Companion Phase 1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

_TRACKS = ("memory_mode", "voice_mode", "presence_mode", "gemini_live_integration")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _status_file() -> Path:
    return Path(__file__).resolve().parents[1] / ".state" / "evolution_status.json"


def _default_status() -> Dict[str, object]:
    now = _utc_now()
    return {
        "phase": "v3.2-phase1-spaces-first",
        "updated_at": now,
        "tracks": {
            "memory_mode": {
                "state": "active",
                "next_action": "Implement memory schema versioning and journal retrieval endpoints",
                "plan": "plans/FULL_MEMORY_MODE_PLAN.md",
                "started_at": now,
            },
            "voice_mode": {
                "state": "active",
                "next_action": "Harden voice UX start/stop with explicit fallback states",
                "plan": "plans/FULL_VOICE_MODE_PLAN.md",
                "started_at": now,
            },
            "presence_mode": {
                "state": "active",
                "next_action": "Refine presence pacing templates and response cadence controls",
                "plan": "plans/FULL_PRESENCE_MODE_PLAN.md",
                "started_at": now,
            },
            "gemini_live_integration": {
                "state": "active_blocked",
                "next_action": "Wire feature-flagged live adapter and wait for Gemini API key",
                "plan": "plans/FULL_GEMINI_LIVE_INTEGRATION_PLAN.md",
                "blocker": "Missing Gemini Live credentials",
                "started_at": now,
            },
        },
    }


def load_or_init_status() -> Dict[str, object]:
    path = _status_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        payload = _default_status()
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        payload = _default_status()

    tracks = payload.get("tracks") if isinstance(payload, dict) else None
    if not isinstance(tracks, dict):
        payload = _default_status()
        tracks = payload["tracks"]

    default_tracks = _default_status()["tracks"]
    for key in _TRACKS:
        if key not in tracks or not isinstance(tracks.get(key), dict):
            tracks[key] = default_tracks[key]

    payload["phase"] = payload.get("phase", "v3.2-phase1-spaces-first")
    payload["updated_at"] = _utc_now()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def set_track_state(track: str, state: str, next_action: str | None = None) -> Dict[str, object]:
    payload = load_or_init_status()
    if track not in payload["tracks"]:
        raise ValueError(f"unknown track: {track}")

    track_state = payload["tracks"][track]
    track_state["state"] = state
    if next_action:
        track_state["next_action"] = next_action
    payload["updated_at"] = _utc_now()

    _status_file().write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
