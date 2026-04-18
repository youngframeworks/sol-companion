# Workflow: Copilot Spaces Blueprint for Sol OS

## Purpose
Define a persistent Copilot Space layout that turns Sol OS into a browser-accessible
mission control surface with stable context across sessions/devices.

## Space Name
`Sol OS Mission Control`

## Pinned Repositories
1. `youngframeworks/aistudio`
2. `youngframeworks/sol-companion`
3. `youngframeworks/sol-os-cloud`

## Pinned Agent
- `SolManagerCloudAgent` (custom Copilot Cloud Agent)

## Pinned Artifacts
- `sol-os-cloud/OS_MANIFEST.md`
- `sol-os-cloud/OS_EVOLUTION_LOG.md`
- `sol-os-cloud/os/workflows/review_project_architecture.workflow.md`
- `sol-os-cloud/os/workflows/self_heal.workflow.md`
- `sol-os-cloud/os/workflows/self_evolve.workflow.md`
- `sol-os-cloud/os/workflows/autosync.workflow.md`
- `sol-os-cloud/os/policies/governance.policy.md`
- `sol-os-cloud/os/policies/models.policy.md`

## Persistent Context Blocks

### Block 1: Current OS Version
- Source: `OS_MANIFEST.md`
- Snapshot fields: version, command surface, critical constraints

### Block 2: Drift Dashboard
- Per project drift score
- Last architecture review timestamp
- Last autosync PR status

### Block 3: Evolution Dashboard
- Last 5 entries from `OS_EVOLUTION_LOG.md`
- Performance notes trend
- Pending vNext proposals

### Block 4: Governance Guardrails
- Human-gate phrases
- No-force-push, no-auto-merge
- OS boundary rules

## Session Starters
- "Run architecture review for sol-companion and summarize drift score."
- "Run autosync plan for all projects and propose PR branches."
- "Propose v3.2 evolution cycle based on latest performance notes."
- "Show model recommendations by task type and workflow."

## Constraints
- Space operations are proposal-first.
- Write actions require explicit human confirmation.
- Never modify outside mirror paths during autosync.
- All proposed changes must include rollback notes.

## Validation Checklist
- Agent can resolve all pinned files.
- Drift dashboard values match latest review outputs.
- Autosync suggestions reference actual changed files.
- Governance constraints appear in every write proposal.
