---
name: inventory-reconciliation
description: Identify supplied inventory counts that do not cover requested order quantities.
---
# Inventory Reconciliation
## Tool: classify-fulfillment-exceptions
### Inputs and Data Sources
Order item SKU and quantity plus supplied available inventory.
### Decision and Reasoning
Compare requested quantity with available quantity only when SKU data matches.
### Outputs and Evidence
Include SKU, requested quantity, and supplied available quantity.
### Limits and Constraints
No reservation, allocation, or substitution is performed.
### Failure Handling
Unparseable quantities are not used as proof of shortage.
### Human Review
Warehouse staff verify current stock and approved backorder options.
