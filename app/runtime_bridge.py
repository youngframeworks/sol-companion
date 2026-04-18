"""Runtime bridge that keeps Sol Companion separate while reusing AI Studio OS services."""

from __future__ import annotations

import sys
from pathlib import Path


def bootstrap_paths() -> None:
    """Allow imports from the sibling aistudio project without copying its code."""
    companion_root = Path(__file__).resolve().parents[1]
    workspace_root = companion_root.parent
    aistudio_root = (workspace_root / "aistudio").resolve()
    if str(aistudio_root) not in sys.path:
        sys.path.insert(0, str(aistudio_root))


bootstrap_paths()


try:
    from adk_app.agents.base_agent import BaseAgent  # type: ignore
except Exception:  # pragma: no cover - fallback for current runtime shape
    class BaseAgent:
        """Fallback base class when the host runtime does not expose one yet."""

        async def run(self, *args, **kwargs):
            raise NotImplementedError


try:
    from adk_app.workflows.base_workflow import BaseWorkflow  # type: ignore
except Exception:  # pragma: no cover - fallback for current runtime shape
    class BaseWorkflow:
        """Fallback base class when the host runtime does not expose one yet."""

        async def run(self, *args, **kwargs):
            raise NotImplementedError


from adk_app.compat.path_resolver import os_root_summary
from adk_app.main import session_service
from adk_app.models.registry import registry
from adk_app.services.logger import Logger
from adk_app.services.runtime_paths import bootstrap_project_runtime

# Ensure runtime path env vars are available before server boot.
bootstrap_project_runtime()
