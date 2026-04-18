# Policy: Atomic Operations

## Rules
1. Group changes by single intent.
2. Keep patch sets reversible.
3. Record preconditions and postconditions.
4. Do not mix unrelated scope in one operation.

## Rollback
- Every workflow must define rollback points before write steps.
