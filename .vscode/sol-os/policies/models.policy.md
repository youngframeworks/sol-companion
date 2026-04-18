# Policy: models

## Purpose
Define which local model is appropriate for each task category, how model selection
is governed, and what constraints apply to the local model runtime.

## Canonical Model Store
- **Path:** `models/gguf/` (repo root)
- **Rule:** This is the single source of truth. No copies elsewhere.
- **Rule:** GGUF files must never be committed to Git (`models/gguf/` is in `.gitignore`).

## Registered Models

| Alias | File | Port | Best For |
|---|---|---|---|
| `qwen3.5:2b` | `Qwen2.5-3B-Instruct-Q4_K_M.gguf` | 8081 | General instruction following, planning, task intake |
| `gemma4:e2b` | `gemma-2-2b-it-Q4_K_M.gguf` | 8082 | Code review, structured output, policy validation |
| `llama3.2:1b` | `Llama-3.2-1B-Instruct-Q4_K_M.gguf` | 8083 | Fast classification, routing, short-context tasks |
| `qwen2.5-coder:1.5b` | `Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf` | 8084 | Code generation, patch authoring, syntax validation |

## Selection Rules

1. **Code generation / patching** → `qwen2.5-coder:1.5b` (port 8084). Highest code accuracy.
2. **Routing / classification** → `llama3.2:1b` (port 8083). Lowest latency.
3. **Planning / structured task intake** → `qwen3.5:2b` (port 8081). Best instruction following.
4. **Review / policy / validation** → `gemma4:e2b` (port 8082). Best at structured critique.
5. **Default** → `qwen3.5:2b` when task type is unclear.

## Preferred Model Per Task Type (v3.1)

This matrix maps Sol OS workflow steps to the recommended local model.
Use this during `self-evolve` model recommendation scans.

| Task type | Preferred model | Rationale |
|---|---|---|
| Task intake / Issue parsing | `qwen3.5:2b` | Strong at instruction following and structured extraction |
| Architecture review | `gemma4:e2b` | Best structured critique and policy validation |
| Feature planning / decomposition | `qwen3.5:2b` | Reliable multi-step reasoning |
| Code patch generation | `qwen2.5-coder:1.5b` | Purpose-built for code; lowest hallucination rate on syntax |
| Code review / diff analysis | `qwen2.5-coder:1.5b` | Understands code semantics |
| Refactor planning | `qwen3.5:2b` | Better at reasoning about intent vs implementation |
| Test generation | `qwen2.5-coder:1.5b` | Accurate test scaffolding |
| Routing / intent classification | `llama3.2:1b` | Fastest; sufficient for binary/multi-class routing |
| Policy validation | `gemma4:e2b` | Structured output, low false-positive rate |
| Self-heal proposal generation | `gemma4:e2b` | Conservative and policy-aware |
| Self-evolve opportunity analysis | `qwen3.5:2b` | Broad reasoning across many file types |
| Commit message / PR summary | `qwen3.5:2b` | Concise, conventional output |

## Model Change Policy

When proposing a model change (via `self-evolve`):
1. State the task type and current assignment.
2. Provide evidence: benchmark reference, observed failure mode, or latency data.
3. Log the change in `OS_EVOLUTION_LOG.md` under the version entry.
4. Update both this table and `adk_app/config/models.yaml`.

## Runtime Rules

- All model servers are **local validation only**. They are never the production execution path.
- Copilot Cloud models are always the primary execution engine.
- Local models activate when: user explicitly requests `test locally`, or `self-heal` proposes validation.
- A model is healthy if its port responds to `GET /v1/models` within 3 seconds.
- If a model server is not running, the workflow continues with a warning; it does not block execution.

## Adding / Replacing Models

1. Download GGUF to `models/gguf/`.
2. Add entry to `adk_app/config/models.yaml`.
3. Add `start_server` line to `llama.cpp/llamacpp_start.sh`.
4. Update this policy table.
5. Re-sync: `sol sync-os`.

## Constraints

- Never download models to `llama.cpp/models/` or any path other than `models/gguf/`.
- Never commit `.gguf` files.
- Port assignments are fixed (8081–8084); request a new port via `sol load-task` Issue if expanding.
