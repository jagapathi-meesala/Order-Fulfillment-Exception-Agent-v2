# Explainability and Decision Transparency

## Purpose
This document explains the inputs, rules, evidence, outputs, limitations, and human-review requirements of the Order Fulfillment Exception Agent. Every finding must be traceable to supplied data and an explicit rule.

## Inputs
The agent accepts supplied order records, inventory records, shipment records, and optional configuration.

Order data may include order ID, order status, payment status, and requested quantities. Inventory data may include product identifiers and available quantities. Shipment data may include carrier status and the timestamp of the latest event.

The agent does not assume that missing information proves that an event did not happen. Timestamps must be parseable before they are used in delay calculations.

## Decision and Reasoning
The agent validates input records before classifying exceptions. It applies deterministic rules to the supplied data.

- Missing required fields and duplicate order identifiers are reported as validation issues.
- Pending or unconfirmed payment status can produce a payment exception.
- Insufficient available inventory can produce an inventory shortage finding.
- A shipment explicitly marked as an exception can produce a carrier exception finding.
- An in-transit shipment can be flagged as stale when a valid event timestamp, reference time, and configured delay threshold are available and the threshold is exceeded.
- A cancelled order with an active shipment can produce a cancellation-versus-shipment finding.

Each finding includes an order identifier when available, a reason code, severity, supporting evidence, a recommended action, and a human-review indicator. A finding is not proof of wrongdoing or a guarantee that an order is delayed.

## Severity and Prioritization
Severity is assigned according to the implemented rule and supplied evidence. High severity indicates an exception that warrants prompt review; medium severity indicates an issue that should be checked. Severity is a triage aid, not a measured probability or a substitute for operational policy.

## Outputs and Evidence
The report is JSON and includes an overall status, a summary of processed orders and findings, input validation issues, individual findings, evidence, recommended actions, and limitations.

Evidence should identify the input values and calculations supporting the finding. For example, a stale-transit finding may include the last event timestamp, calculated hours since the event, and configured threshold.

The report must not claim that an external system was checked when no external lookup was performed.

## Tool: validate-order-data

### Inputs and Data Sources
Accepts the supplied order records. It does not fetch orders from an external order-management system.

### Decision and Reasoning
Checks required order fields and identifies duplicate order identifiers according to the implemented validation rules. Missing or malformed information is reported rather than silently invented.

### Outputs and Evidence
Returns validation issues with the available record context and a description of the problem.

### Limits and Constraints
Validation is limited to the fields and rules implemented by the tool. A record passing validation does not guarantee that the order is operationally correct.

### Failure Handling
Invalid input structure or missing required data must be reported clearly. The agent must not fabricate replacement identifiers or missing values.

### Human Review
An operator should correct or verify the source record before relying on downstream exception findings.

## Tool: classify-fulfillment-exceptions

### Inputs and Data Sources
Accepts supplied orders, inventory, shipments, and optional configuration.

### Decision and Reasoning
Applies explicit rules for payment status, inventory availability, shipment exceptions, stale in-transit events, and cancelled orders with active shipments. Delay calculations require valid timestamps and a reference time. Findings are based only on the records provided.

### Outputs and Evidence
Returns findings with reason codes, severity, supporting evidence, recommended actions, and human-review indicators.

### Limits and Constraints
The tool does not independently verify payment settlement, warehouse stock, carrier tracking, delivery completion, or company policies. Missing information can limit the confidence or applicability of a rule.

### Failure Handling
Malformed records, unavailable fields, or unusable timestamps must not be treated as confirmed operational events. Where evidence is insufficient, the result should indicate the limitation or request review.

### Human Review
An operations team member must verify the evidence and determine the appropriate resolution before changing an order, payment, inventory quantity, or shipment.

## Tool: generate-exception-report

### Inputs and Data Sources
Accepts the analysis result produced from the supplied fulfillment records.

### Decision and Reasoning
Organizes the existing validation issues and findings into a structured report. It should preserve reason codes, severity, evidence, recommendations, and limitations rather than inventing new findings.

### Outputs and Evidence
Produces a JSON report containing the overall status, summary counts, validation issues, findings, and limitations. The report is intended for inspection and downstream review.

### Limits and Constraints
Report generation does not independently confirm the correctness of source records or execute recommended actions.

### Failure Handling
If the analysis result is malformed or incomplete, the report should not represent missing findings as a clean result. Invalid input should produce a clear error or validation issue.

### Human Review
The report recipient should verify important findings against the authoritative order, payment, inventory, and shipping systems before taking action.

## Human Review and Operational Safety
All recommendations are advisory. The agent must not automatically cancel orders, issue refunds, change inventory, contact carriers, or modify shipments. Authorized personnel remain responsible for decisions and actions.

## Auditability
Findings should be reproducible from the supplied input records, configuration, reference time, and implemented rules. Changes to thresholds or rules should be documented. Reports should retain enough evidence to explain why each finding was generated.

## Global Limits
- No live order-management, payment-gateway, warehouse, carrier, or policy-database lookups are performed.
- No claim of real-time tracking or external verification is made.
- Delay calculations depend on valid timestamps, a reference time, and the configured threshold.
- Severity is a rule-based triage label, not a probability.
- Recommendations require human review.
