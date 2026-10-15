---
name: shipping-delay-analysis
description: Detect carrier exception states and stale in-transit events from supplied tracking data.
---
# Shipping Delay Analysis
## Tool: classify-fulfillment-exceptions
### Inputs and Data Sources
Supplied carrier status, last event timestamp, and optional reference time.
### Decision and Reasoning
Only calculate event age when timestamps parse and a reference time is configured.
### Outputs and Evidence
Include carrier status, event timestamp, and configured threshold.
### Limits and Constraints
No live tracking or delivery guarantee is available.
### Failure Handling
Ignore unparseable timestamps for age calculation and avoid invented ETAs.
### Human Review
Fulfillment staff check current tracking and decide customer communication.
