from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3, "critical": 4}

def _parse_time(value: Any):
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        return None

def validate_data(data: dict) -> list[dict]:
    issues = []
    if not isinstance(data, dict):
        return [{"code": "INVALID_ROOT", "severity": "high", "message": "Input must be a JSON object."}]
    orders = data.get("orders", [])
    if not isinstance(orders, list):
        return [{"code": "INVALID_ORDERS", "severity": "high", "message": "orders must be a list."}]
    seen = set()
    for index, order in enumerate(orders):
        if not isinstance(order, dict):
            issues.append({"code": "INVALID_ORDER_ROW", "severity": "medium", "message": f"Order row {index} is not an object."})
            continue
        oid = order.get("order_id")
        if not isinstance(oid, str) or not oid.strip():
            issues.append({"code": "MISSING_ORDER_ID", "severity": "high", "message": f"Order row {index} has no valid order_id."})
        elif oid in seen:
            issues.append({"code": "DUPLICATE_ORDER_ID", "severity": "high", "message": f"Duplicate order_id: {oid}.", "order_id": oid})
        else:
            seen.add(oid)
        if "status" not in order:
            issues.append({"code": "MISSING_ORDER_STATUS", "severity": "medium", "message": f"Order row {index} is missing status.", "order_id": oid})
    return issues

def analyze(data: dict) -> dict:
    validation = validate_data(data)
    if not isinstance(data, dict):
        return {"status": "invalid_input", "summary": {"orders": 0, "findings": 0, "validation_issues": len(validation)}, "validation_issues": validation, "findings": []}
    orders = data.get("orders", [])
    if not isinstance(orders, list):
        return {"status": "invalid_input", "summary": {"orders": 0, "findings": 0, "validation_issues": len(validation)}, "validation_issues": validation, "findings": []}
    cfg = data.get("config") if isinstance(data.get("config"), dict) else {}
    threshold = cfg.get("in_transit_delay_hours", 72)
    try:
        threshold = max(0, float(threshold))
    except (TypeError, ValueError):
        threshold = 72.0
    reference = _parse_time(cfg.get("reference_time"))
    inventory = {}
    for row in data.get("inventory", []) if isinstance(data.get("inventory", []), list) else []:
        if isinstance(row, dict) and isinstance(row.get("sku"), str):
            try: inventory[row["sku"]] = float(row.get("available", 0))
            except (TypeError, ValueError): inventory[row["sku"]] = None
    shipments = {}
    for row in data.get("shipments", []) if isinstance(data.get("shipments", []), list) else []:
        if isinstance(row, dict) and row.get("order_id") is not None:
            shipments[row["order_id"]] = row
    findings = []
    def add(order_id, code, severity, evidence, action):
        findings.append({"order_id": order_id, "code": code, "severity": severity, "evidence": evidence, "recommended_action": action, "requires_human_review": True})
    for order in orders:
        if not isinstance(order, dict): continue
        oid = order.get("order_id")
        if str(order.get("payment_status", "")).strip().lower() in {"pending", "failed", "unpaid"}:
            add(oid, "PAYMENT_NOT_CONFIRMED", "high" if str(order.get("payment_status")).lower() == "failed" else "medium", {"payment_status": order.get("payment_status")}, "Verify payment gateway status and applicable payment policy.")
        for item in order.get("items", []) if isinstance(order.get("items", []), list) else []:
            if not isinstance(item, dict): continue
            sku = item.get("sku")
            try: qty = float(item.get("quantity", 0))
            except (TypeError, ValueError): qty = 0
            if sku in inventory and inventory[sku] is not None and qty > inventory[sku]:
                add(oid, "INVENTORY_SHORTAGE", "high", {"sku": sku, "requested_quantity": qty, "supplied_available_quantity": inventory[sku]}, "Reconcile warehouse availability and check approved backorder or substitution options.")
        shipment = shipments.get(oid)
        if shipment:
            carrier_status = str(shipment.get("carrier_status", "")).strip().lower()
            if carrier_status in {"exception", "delivery_exception", "failed_attempt", "held"}:
                add(oid, "CARRIER_EXCEPTION", "high", {"carrier_status": shipment.get("carrier_status"), "last_event_at": shipment.get("last_event_at")}, "Review the latest carrier event and confirm the approved resolution path.")
            elif carrier_status in {"in_transit", "in transit", "transit"} and reference:
                event_time = _parse_time(shipment.get("last_event_at"))
                if event_time and (reference - event_time).total_seconds() > threshold * 3600:
                    hours = round((reference - event_time).total_seconds() / 3600, 1)
                    add(oid, "STALE_IN_TRANSIT", "medium", {"last_event_at": shipment.get("last_event_at"), "hours_since_event": hours, "configured_threshold_hours": threshold}, "Check carrier tracking for new scans and assess whether customer communication is needed.")
        if str(order.get("status", "")).strip().lower() in {"cancelled", "canceled"} and shipment and str(shipment.get("carrier_status", "")).lower() not in {"", "cancelled", "canceled"}:
            add(oid, "CANCELLED_ORDER_HAS_SHIPMENT", "high", {"order_status": order.get("status"), "carrier_status": shipment.get("carrier_status")}, "Confirm cancellation and shipment state with the responsible operations team.")
    findings.sort(key=lambda x: (-SEVERITY_ORDER.get(x["severity"], 0), str(x.get("order_id", "")), x["code"]))
    status = "review_required" if findings or validation else "no_exceptions_detected"
    return {"status": status, "summary": {"orders": len(orders), "findings": len(findings), "validation_issues": len(validation)}, "validation_issues": validation, "findings": findings, "limits": ["Uses only supplied records; no live carrier or warehouse lookups.", "Recommendations are advisory and require human review."]}
