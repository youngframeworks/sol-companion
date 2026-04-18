"""FastAPI server for Sol Companion."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .evolution import load_or_init_status, set_track_state
from .runtime_bridge import Logger, os_root_summary
from .sol_workflow import SolCompanionWorkflow

app = FastAPI(title="Sol Companion", version="1.0.0")
workflow = SolCompanionWorkflow()


class SolRequest(BaseModel):
    message: str
    session_id: str | None = "sol-default"
    mode: str | None = "companion"
    breath_grounding: bool | None = False


class ResetRequest(BaseModel):
    session_id: str | None = "sol-default"


class SummaryRequest(BaseModel):
    session_id: str | None = "sol-default"


class EvolutionTrackRequest(BaseModel):
    track: str
    state: str = "active"
    next_action: str | None = None


VALID_MODES = {"companion", "presence", "insight", "journal", "memory", "voice", "gemini_live"}


@app.on_event("startup")
async def on_startup() -> None:
    status = load_or_init_status()
    Logger.log(
        "Sol Companion startup",
        {
            "os_governance": os_root_summary(),
            "workflow": "User -> SolCompanionAgent -> Response",
            "evolution_phase": status.get("phase"),
        },
    )


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html_path = Path(__file__).resolve().parent / "ui" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.post("/sol")
async def run_sol(payload: SolRequest) -> dict:
    text = payload.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="message cannot be empty")

    mode = (payload.mode or "companion").strip().lower()
    if mode not in VALID_MODES:
        raise HTTPException(status_code=400, detail=f"mode must be one of: {', '.join(sorted(VALID_MODES))}")

    result = await workflow.run(
        text,
        session_id=payload.session_id or "sol-default",
        mode=mode,
        breath_grounding=bool(payload.breath_grounding),
    )
    return {
        "response": result["response"],
        "session_id": result["session_id"],
        "history_len": result["history_len"],
        "mode": result["mode"],
    }


@app.post("/sol/reset")
async def reset_sol(payload: ResetRequest | None = None) -> dict:
    session_id = "sol-default"
    if payload and payload.session_id:
        session_id = payload.session_id

    result = await workflow.reset_space(session_id=session_id)
    return {"status": result["status"], "session_id": result["session_id"]}


@app.post("/sol/summary")
async def session_summary(payload: SummaryRequest | None = None) -> dict:
    session_id = "sol-default"
    if payload and payload.session_id:
        session_id = payload.session_id
    summary = await workflow.session_summary(session_id=session_id)
    return summary


@app.get("/sol/modes")
async def list_modes() -> dict:
    return {
        "modes": ["companion", "presence", "insight", "journal", "memory", "voice", "gemini_live"],
        "grounding": ["breath"],
    }


@app.get("/sol/evolution/status")
async def evolution_status() -> dict:
    return load_or_init_status()


@app.post("/sol/evolution/start")
async def evolution_start(payload: EvolutionTrackRequest) -> dict:
    status = set_track_state(payload.track, payload.state, payload.next_action)
    return {
        "status": "ok",
        "track": payload.track,
        "state": status["tracks"][payload.track]["state"],
        "updated_at": status["updated_at"],
    }


@app.get("/sol/dependency-graph")
async def dependency_graph() -> dict:
    mermaid = """
graph TD
  User[User UI] --> Server[sol_server.py]
  Server --> Workflow[sol_workflow.py]
  Workflow --> Agent[sol_agent.py]
  Agent --> Memory[.state/sol_memory.json]
  Agent --> Registry[aistudio/adk_app registry]
  Server --> Bridge[runtime_bridge.py]
  Bridge --> ADK[aistudio ADK runtime]
  Voice[Voice Mode] --> Server
  Presence[Presence Mode] --> Agent
  MemoryMode[Memory Mode] --> Agent
  Gemini[Gemini Live Integration] --> Server
""".strip()
    return {"format": "mermaid", "graph": mermaid}
