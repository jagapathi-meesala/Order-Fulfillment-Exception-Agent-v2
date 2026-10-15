# Explainability and Decision Transparency

## Purpose
Explain how the Order Fulfillment Exception Agent validates records, identifies exceptions, assigns severity, and recommends actions. Every finding must be traceable to supplied data and an implemented rule.

## Inputs
Inputs include supplied order records, inventory records, shipment records, and optional configuration. Relevant fields may include order identifiers, order status, payment status, requested quantities, available quantities, carrier status, event timestamps, a reference time, and a configured delay threshold.

Missing data is not proof that an event did not happen. The agent must not invent missing values.

## Decision
The agent validates records before classifying exceptions. It applies deterministic rules to supplied evidence:
- Missing required fields or duplicate order identifiers produce validation issues.
- Pending payment can produce a payment exception.
- Insufficient supplied inventory can produce an inventory shortage.
- A shipment explicitly marked as an exception can produce a carrier exception.
- An in-transit shipment can be flagged as stale when valid timestamps and a configured threshold establish that the threshold was exceeded.
- A cancelled order with an active shipment can produce a status-conflict finding.

The exact findings depend on the implemented rules and input values. A finding is not proof that an external system was checked.

## Severity and Prioritization
Severity is a rule-based triage label. High severity calls for prompt review; medium severity calls for investigation. Severity is not a probability or a guarantee of operational impact.

## Outputs and Evidence
The JSON report includes a status, summary counts, validation issues, findings, evidence, recommended actions, human-review indicators, and limitations. A finding should identify its order when possible, reason code, severity, supporting input values or calculations, and recommended next step.

## Tool: validate_order_data

### Inputs and Data Sources
Receives supplied order records. It does not fetch orders from an external system.

### Decision and Reasoning
Checks required fields and duplicate order identifiers using the implemented validation rules. Missing or malformed values are reported rather than guessed.

### Outputs and Evidence
Returns validation issues with available record context and a description of each problem.

### Limits and Constraints
Validation only covers implemented rules and supplied fields. Passing validation does not prove that an order is correct.

### Failure Handling
Malformed input or missing required data must be reported clearly. The agent must not fabricate identifiers or silently replace missing values.

### Human Review
An operator should correct or verify affected source records before relying on downstream findings.

## Tool: classify_fulfillment_exceptions

### Inputs and Data Sources
Receives supplied orders, inventory, shipments, and optional configuration.

### Decision and Reasoning
Applies implemented rules for payment status, inventory shortages, carrier exceptions, stale transit, and cancelled orders with active shipments. Stale-transit calculations require usable timestamps, a reference time, and a configured threshold.

### Outputs and Evidence
Returns findings with reason codes, severity, supporting evidence, recommended actions, and human-review indicators.

### Limits and Constraints
The tool does not independently verify payment settlement, warehouse stock, carrier tracking, delivery completion, or company policies. Conclusions are limited to supplied records and implemented rules.

### Failure Handling
Invalid records, missing fields, or unusable timestamps must not be treated as confirmed operational events. Insufficient evidence must be reported or sent for review.

### Human Review
An authorized operations team member must verify important findings before changing an order, payment, inventory quantity, or shipment.

## Tool: generate_exception_report

### Inputs and Data Sources
Receives the analysis result and findings produced from supplied fulfillment records.

### Decision and Reasoning
Organizes existing validation issues and findings into a structured report. It must preserve evidence, severity, reason codes, recommendations, and limitations instead of inventing findings.

### Outputs and Evidence
Produces a JSON report containing status, summary counts, validation issues, findings, evidence, recommended actions, and limitations.

### Limits and Constraints
Report generation does not independently verify source records or execute recommended actions.

### Failure Handling
Malformed or incomplete analysis results must not be presented as a confirmed clean result. Invalid input should produce a clear error or validation issue.

### Human Review
The recipient should verify findings against authoritative order, payment, inventory, and shipping systems before taking action.

## Human Review and Safety
All recommendations are advisory. The agent must not automatically cancel orders, issue refunds, modify inventory, contact carriers, or change shipments. Authorized personnel remain responsible for operational decisions.

## Auditability
Findings should be reproducible from the supplied records, configuration, reference time, and implemented rules. Threshold or rule changes should be documented. Reports should retain enough evidence to explain why each finding was generated.

## Global Limits
- No live order, payment, warehouse, carrier, or policy-system lookups are performed.
- No real-time tracking or external verification is claimed.
- Delay calculations depend on valid timestamps, a reference time, and configuration.
- Severity is a rule-based triage label, not a probability.
- Recommendations require human review.
