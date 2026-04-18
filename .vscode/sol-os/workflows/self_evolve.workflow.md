# Workflow: self_evolve

## Trigger
- Chat: `@SolManagerAgent self evolve`
- CLI: `sol self-evolve`

## Purpose
Analyse the current state of Cloud OS contracts (agents, workflows, policies, scripts,
CLI) and propose targeted improvements: simplifications, automation gains, ergonomic
wins, and alignment improvements. Generate a versioned patch only when the user approves.
Record every accepted evolution in `OS_EVOLUTION_LOG.md`.

## Responsible Agent
SolManagerAgent (analysis and patch coordination)
→ ArchitectAgent (design review)
→ ImplementerAgent (patch generation)
→ GitOpsAgent (commit message + PR)

## Inputs
- All `sol-os-cloud/os/` contracts
- `sol-os-cloud/scripts/sol` (CLI)
- `.vscode/copilot-agents/SolManagerAgent.agent.md`
- `sol-os-cloud/OS_MANIFEST.md`
- `sol-os-cloud/OS_EVOLUTION_LOG.md`
- Recent GitHub Issues and PR history (if available via `github-pull-request_doSearch`)
- `adk_app/config/models.yaml` (for model registration alignment check)

## Sequence

1. **Analyse** (read-only)
   - Agent definitions: gaps, outdated tools, verbose or duplicate sections
   - Workflows: missing triggers, overly complex chains, missing constraints
   - Policies: contradictions, gaps, outdated rules
   - Scripts: duplicated logic, inconsistent error handling, missing features
   - CLI: missing aliases, commands not wired in `sol` script, help text gaps

   **Performance sub-scan (v3.1):**
   - Identify "slow paths": multi-agent chains with ≥ 4 hops where fewer would suffice
   - Flag heavy prompts: agent definitions > 300 lines or workflow sequences > 8 steps
   - Note any workflow that invokes both AIStudio and Copilot Cloud unnecessarily
   - Recommend: prompt compression, chain shortening, or caching opportunities

   **Prompt optimisation sub-scan (v3.1):**
   - Review agent `description` and `argument-hint` for clarity and brevity
   - Identify redundant sections duplicated across agents or workflows
   - Propose before/after diff for any prompt change; require rollback note

   **Model recommendation scan (v3.1):**
   - Cross-check `adk_app/config/models.yaml` against `models.policy.md`
   - Flag any task type in workflows not covered by a model selection rule
   - Propose `models.policy.md` additions if coverage gaps found

2. **Score opportunities**
   - Impact: `high` | `medium` | `low`
   - Risk: `safe` | `review needed` | `breaking`
   - Effort: `trivial` | `minor` | `significant`

3. **Propose evolution plan**
   Present structured report:

```
## Self-Evolve Proposal — <timestamp>

### Analysis Summary
...

### Performance Findings
| Path | Hops | Recommended | Saving |
|---|---|---|---|

### Prompt Optimisation Candidates
| File | Issue | Before (excerpt) | After (excerpt) | Rollback |
|---|---|---|---|---|

### Model Coverage Gaps
| Task type | Currently unassigned | Recommended model |
|---|---|---|

### Evolution Opportunities
| ID | Area | Description | Impact | Risk | Effort |
|----|------|-------------|--------|------|--------|

### Proposed Patch
#### Evolution E-XX: <title>
- Files affected: <list>
- Change summary: <description>
- Justification: <why this improves the OS>
- Rollback: revert <file> to <previous state>

### Version bump
Current: <version>  →  Proposed: <new version>

### ⚠️ Human gate — changes are NOT applied until you confirm.
Reply: "Apply evolution" (all) or "Apply E-01, E-03" (selective)
```

4. **Apply** (only after confirmation)
   - Apply each confirmed evolution atomically.
   - Increment OS version in `OS_MANIFEST.md`.
   - Append entry to `sol-os-cloud/OS_EVOLUTION_LOG.md`:

```markdown
## <version> — <date>
**Changes:** <list>
**Reason:** <why>
**Impact:** <what improved>
**PERFORMANCE_NOTES:** <latency/chain improvements made, or "none">
```

5. **Re-sync**
   Run: `bash sol-os-cloud/scripts/sync_os_to_project.sh --target all`

6. **Commit**
   GitOpsAgent generates: `feat(sol-os): <conventional commit message>`

## Constraints
- **Never auto-apply.** Every evolution requires explicit confirmation with the exact phrase "Apply evolution" or "Apply E-NN".
- Patches must NOT be generated until confirmation is received. Proposals are read-only plans.
- Never break existing command surfaces without a migration note.
- Version bumps follow semver: patch for fixes, minor for new capability, major for breaking.
- Every applied evolution must be logged in `OS_EVOLUTION_LOG.md` with `PERFORMANCE_NOTES`.
- Self-evolve must not exceed 5 proposed changes per invocation (batching).
- Prompt changes require: before/after diff + rollback note. No exceptions.
