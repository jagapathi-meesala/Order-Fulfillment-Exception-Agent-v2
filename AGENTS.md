# Agent Operating Guide
## Inputs
A JSON object with `orders` and optional `inventory`, `shipments`, and `config`. Orders should include `order_id`, `status`, and optionally `payment_status`, `items`, and `created_at`. Inventory rows use `sku` and `available`. Shipment rows use `order_id`, `carrier_status`, and optionally `last_event_at`.
## Decision
Validate records, associate shipments and inventory where identifiers match, classify each observed exception using configured thresholds, and attach evidence plus a human-review action.
## Limits
This is a deterministic triage aid, not an order-management system. It does not query live stores or carriers and cannot guarantee delivery estimates. No destructive or external action is performed.
