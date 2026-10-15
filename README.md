# Order Fulfillment Exception Agent

A local Python agent for triaging order fulfillment exceptions from supplied JSON data. It validates records, detects common fulfillment risks, and emits evidence-backed recommendations without modifying orders or contacting external services.

## Features
- Missing/duplicate order identifier and invalid field checks
- Payment-pending, inventory-shortage, shipment-exception, and stale-in-transit detection
- Severity levels and reason codes with evidence
- JSON report output and a small example dataset
- Unit tests and a readiness audit

## Run
```bash
python3 -m unittest discover -s tests -v
python3 verification/readiness_audit.py
python3 -m core.cli examples/fulfillment_case.json --output report.json
```

No third-party dependencies are required. All outputs are recommendations for human review. The agent does not perform fulfillment actions or access live carrier/warehouse systems.
