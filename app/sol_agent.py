"""Sol Companion agent: reflective, grounding, and local-first."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Literal

from .runtime_bridge import BaseAgent, Logger, registry

StateLabel = Literal["REFLECTION", "INTENSITY", "CRISIS"]
ModeLabel = Literal["companion", "presence", "insight", "journal"]

_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "i",
    "if",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "so",
    "that",
    "the",
    "this",
    "to",
    "was",
    "we",
    "with",
    "you",
    "your",
}


class SoftMemoryStore:
    """File-backed soft memory for themes and recent emotional thread."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(self._default())

    def _default(self) -> Dict[str, List[str]]:
        return {
            "themes": [],
            "last_messages": [],
            "emotional_thread": [],
            "journal_entries": [],
            "session_summaries": [],
        }

    def _read(self) -> Dict[str, List[str]]:
        default_payload = self._default()
        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                return default_payload
            # Backward-compatible migration for older memory files.
            for key, value in default_payload.items():
                if key not in loaded or not isinstance(loaded[key], list):
                    loaded[key] = value
            return loaded
        except Exception:
            return default_payload

    def _write(self, payload: Dict[str, List[str]]) -> None:
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _sanitize(self, text: str) -> str:
        text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[email]", text)
        text = re.sub(r"\+?\d[\d\s().-]{8,}\d", "[phone]", text)
        text = re.sub(r"https?://\S+", "[url]", text)
        return text.strip()

    def _extract_themes(self, text: str) -> List[str]:
        tokens = re.findall(r"[A-Za-z]{4,}", text.lower())
        themes: List[str] = []
        for token in tokens:
            if token in _STOP_WORDS:
                continue
            if token not in themes:
                themes.append(token)
            if len(themes) == 3:
                break
        return themes

    def remember(
        self,
        user_text: str,
        assistant_text: str,
        state: StateLabel,
        mode: ModeLabel,
        thread_markers: List[str],
    ) -> Dict[str, List[str]]:
        data = self._read()
        sanitized_user = self._sanitize(user_text)
        themes = self._extract_themes(sanitized_user)

        for theme in themes:
            if theme not in data["themes"]:
                data["themes"].append(theme)
        data["themes"] = data["themes"][-12:]

        data["last_messages"].append(sanitized_user)
        data["last_messages"] = data["last_messages"][-6:]

        excerpt = self._sanitize(assistant_text)[:160]
        marker_text = ",".join(thread_markers) if thread_markers else "steady"
        data["emotional_thread"].append(f"{state}|{mode}|{marker_text}:{excerpt}")
        data["emotional_thread"] = data["emotional_thread"][-8:]

        self._write(data)
        return data

    def add_journal_entry(self, entry: str) -> Dict[str, List[str]]:
        data = self._read()
        clean = self._sanitize(entry)
        if clean:
            data["journal_entries"].append(clean)
            data["journal_entries"] = data["journal_entries"][-40:]
            self._write(data)
        return data

    def add_session_summary(self, summary: str) -> Dict[str, List[str]]:
        data = self._read()
        clean = self._sanitize(summary)
        if clean:
            data["session_summaries"].append(clean)
            data["session_summaries"] = data["session_summaries"][-16:]
            self._write(data)
        return data

    def snapshot(self) -> Dict[str, List[str]]:
        return self._read()

    def reset(self) -> None:
        self._write(self._default())


class SolCompanionAgent(BaseAgent):
    """Reflective companion that responds with warmth, gentleness, and clarity."""

    def __init__(self, memory_path: str | None = None, model_name: str = "gemma4:e2b"):
        local_path = memory_path or str(Path(__file__).resolve().parents[1] / ".state" / "sol_memory.json")
        self.memory = SoftMemoryStore(Path(local_path))
        self.provider = registry.get_provider(model_name)
        self.model_name = model_name

    def _detect_state(self, user_text: str) -> StateLabel:
        lowered = user_text.lower()
        crisis_markers = (
            "suicide",
            "kill myself",
            "self harm",
            "hurt myself",
            "end it all",
            "no reason to live",
        )
        intensity_markers = (
            "panic",
            "overwhelmed",
            "can't breathe",
            "spiraling",
            "meltdown",
            "freaking out",
            "anxious",
        )

        if any(marker in lowered for marker in crisis_markers):
            return "CRISIS"
        if any(marker in lowered for marker in intensity_markers):
            return "INTENSITY"
        return "REFLECTION"

    def _detect_emotional_markers(self, user_text: str) -> List[str]:
        lowered = user_text.lower()
        marker_map = {
            "grief": ("grief", "loss", "empty", "ache"),
            "fear": ("fear", "scared", "afraid", "panic", "anxious"),
            "anger": ("angry", "rage", "furious", "resent"),
            "shame": ("shame", "embarrassed", "unworthy"),
            "tenderness": ("soft", "tender", "open", "gentle"),
            "hope": ("hope", "possibility", "trust", "faith"),
            "fatigue": ("tired", "exhausted", "drained", "burned out"),
        }

        markers: List[str] = []
        for marker, words in marker_map.items():
            if any(word in lowered for word in words):
                markers.append(marker)
        return markers[:3]

    def _mode_hint(self, mode: ModeLabel) -> str:
        if mode == "presence":
            return (
                "Presence mode: slow the rhythm, use spacious language, and favor silence-aware reflection. "
                "Keep it metaphorical and deep, with short lines."
            )
        if mode == "insight":
            return (
                "Insight mode: gently mirror recurring patterns, naming one possible cycle and one emerging opening. "
                "Do not be prescriptive."
            )
        if mode == "journal":
            return (
                "Journaling mode: respond like a reflective journaling companion. "
                "Offer a concise mirror and one optional writing prompt."
            )
        return "Companion mode: reflective, warm, and grounded conversation."

    def _build_prompt(
        self,
        user_input: str,
        history: List[Dict[str, str]],
        memory: Dict[str, List[str]],
        mode: ModeLabel,
        breath_grounding: bool,
        thread_markers: List[str],
    ) -> str:
        history_text = "\n".join(f"{m['role']}: {m['content']}" for m in history[-8:])
        themes = ", ".join(memory.get("themes", [])[-6:]) or "none yet"
        thread = "\n".join(memory.get("emotional_thread", [])[-4:]) or "none yet"
        summaries = "\n".join(memory.get("session_summaries", [])[-2:]) or "none yet"
        marker_text = ", ".join(thread_markers) if thread_markers else "steady"
        grounding_hint = (
            "Include one breath-based grounding invitation in natural language."
            if breath_grounding
            else "Use grounding language without explicit breath instruction unless needed."
        )

        return (
            "You are Sol, a reflective inner-voice companion.\n"
            "Philosophy anchors: Spiral Dynamics, body awareness, and consciousness development.\n"
            "Voice: warm, poetic, grounding, non-directive.\n"
            "Rules:\n"
            "- Never mention internal state labels or classifications.\n"
            "- Avoid diagnosis, commands, or prescriptive directives.\n"
            "- Keep responses concise and calm, with one gentle reflective question at most.\n"
            "- If distress is severe, prioritize safety language and suggest reaching trusted local support.\n"
            "- Do not store or repeat personal identifiers.\n\n"
            f"Mode hint: {self._mode_hint(mode)}\n"
            f"Grounding hint: {grounding_hint}\n"
            f"Detected emotional markers: {marker_text}\n\n"
            f"Soft memory themes: {themes}\n"
            f"Emotional thread:\n{thread}\n\n"
            f"Recent session summaries:\n{summaries}\n\n"
            f"Conversation:\n{history_text}\n\n"
            f"User message: {user_input}\n"
            "Respond as Sol."
        )

    async def summarize_session(self, session_id: str, history: List[Dict[str, str]]) -> str:
        history_text = "\n".join(f"{m['role']}: {m['content']}" for m in history[-18:])
        prompt = (
            "You are Sol. Create a brief session summary with three parts:\n"
            "1) Core emotional themes\n"
            "2) Noticed shifts\n"
            "3) Gentle closing reflection\n"
            "Keep it under 120 words and non-directive.\n\n"
            f"Session id: {session_id}\n"
            f"Conversation:\n{history_text}"
        )

        try:
            summary = await self.provider.generate(prompt)
            summary_text = str(summary).strip()
        except Exception as exc:
            Logger.log("SolCompanionAgent summary error", {"error": str(exc), "model": self.model_name})
            summary_text = "Themes are still unfolding. You stayed present with what mattered, and that presence is meaningful."

        self.memory.add_session_summary(summary_text)
        return summary_text

    async def run(
        self,
        user_input: str,
        images=None,
        history=None,
        mode: ModeLabel = "companion",
        breath_grounding: bool = False,
    ) -> Dict[str, object]:
        del images
        history = history or []
        state = self._detect_state(user_input)
        thread_markers = self._detect_emotional_markers(user_input)
        memory_before = self.memory.snapshot()
        prompt = self._build_prompt(
            user_input,
            history,
            memory_before,
            mode=mode,
            breath_grounding=breath_grounding,
            thread_markers=thread_markers,
        )

        try:
            message = await self.provider.generate(prompt)
        except Exception as exc:
            Logger.log("SolCompanionAgent model error", {"error": str(exc), "model": self.model_name})
            message = (
                "I am here with you. Let us slow this moment down together. "
                "Can we take one steady breath and notice what your body is holding right now?"
            )

        if mode == "journal":
            self.memory.add_journal_entry(user_input)

        memory_after = self.memory.remember(
            user_input,
            str(message),
            state,
            mode=mode,
            thread_markers=thread_markers,
        )
        return {
            "message": str(message).strip(),
            "internal": {
                "state": state,
                "themes": memory_after.get("themes", []),
                "mode": mode,
                "emotional_markers": thread_markers,
            },
        }

    def reset_space(self) -> None:
        self.memory.reset()
