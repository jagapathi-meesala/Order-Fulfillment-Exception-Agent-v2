# Explainability
## Inputs
The report uses the supplied orders, inventory, shipment records, and optional configuration. Missing data is not treated as proof that an event did not happen.
## Decision
Each finding includes a reason code, severity, evidence, and recommended next step. Rules are explicit: unpaid payment status, insufficient supplied inventory, shipment marked exception, or shipment in transit beyond the configured delay threshold.
## Limits
No live API, carrier tracking, warehouse system, or policy database is accessed. Age-based delay is computed only when a parseable timestamp and reference time are supplied. Recommendations require human review.
