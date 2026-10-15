---
name: order-exception-triage
description: Triage order-level fulfillment exceptions with evidence and recommended checks.
---
# Order Exception Triage
## Tool: classify-fulfillment-exceptions
### Inputs and Data Sources
Supplied order and shipment records only.
### Decision and Reasoning
Use explicit status values and report exact evidence fields.
### Outputs and Evidence
Return reason code, severity, evidence, and recommended action.
### Limits and Constraints
No live system access or automatic order changes.
### Failure Handling
Flag missing or malformed fields rather than guessing.
### Human Review
Operations staff confirm any resolution before acting.
