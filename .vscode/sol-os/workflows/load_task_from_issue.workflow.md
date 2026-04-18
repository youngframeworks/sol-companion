# Workflow: Load Task From Issue

## Trigger
`@SolManagerAgent load task`

## Sequence
1. Fetch latest open issue labeled `sol-task`.
2. Normalize request via Task Intake skill.
3. Select feature/bugfix/refactor workflow.
4. Assemble delegated execution plan.
5. Emit patch draft and validation checklist.
