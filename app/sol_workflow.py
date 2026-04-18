"""Single-path workflow for Sol Companion."""

from __future__ import annotations

from typing import Dict

from .sol_agent import ModeLabel

from .runtime_bridge import BaseWorkflow, session_service
from .sol_agent import SolCompanionAgent


class SolCompanionWorkflow(BaseWorkflow):
    """Workflow shape: User -> SolCompanionAgent -> Response."""

    def __init__(self, agent: SolCompanionAgent | None = None):
        self.agent = agent or SolCompanionAgent()
        self.session_service = session_service

    async def run(
        self,
        user_input: str,
        session_id: str = "sol-default",
        mode: ModeLabel = "companion",
        breath_grounding: bool = False,
    ) -> Dict[str, object]:
        self.session_service.add_message(session_id, "user", user_input)
        history = self.session_service.get_history(session_id)

        result = await self.agent.run(
            user_input,
            history=history,
            mode=mode,
            breath_grounding=breath_grounding,
        )
        response_text = str(result.get("message", "")).strip()

        self.session_service.add_message(session_id, "assistant", response_text)
        return {
            "response": response_text,
            "session_id": session_id,
            "history_len": len(self.session_service.get_history(session_id)),
            "mode": mode,
        }

    async def session_summary(self, session_id: str = "sol-default") -> Dict[str, str]:
        history = self.session_service.get_history(session_id)
        summary = await self.agent.summarize_session(session_id, history)
        return {
            "session_id": session_id,
            "summary": summary,
        }

    async def reset_space(self, session_id: str = "sol-default") -> Dict[str, str]:
        self.agent.reset_space()
        self.session_service.clear(session_id)
        return {"status": "ok", "session_id": session_id}
