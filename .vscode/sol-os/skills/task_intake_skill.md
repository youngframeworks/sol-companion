# Skill: Task Intake

## Purpose
Normalize task requests from commands or GitHub Issues into structured execution input.

## Inputs
- Issue title and body
- Labels, assignees, milestone
- Linked artifacts and acceptance criteria

## Output Schema
- `task_type`: feature|bugfix|refactor|ops
- `scope`
- `constraints`
- `acceptance_criteria[]`
- `risks[]`
