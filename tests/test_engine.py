import unittest
from core.engine import analyze, validate_data

class EngineTests(unittest.TestCase):
    def test_payment_pending_detected(self):
        r = analyze({"orders": [{"order_id": "A", "status": "new", "payment_status": "pending"}]})
        self.assertIn("PAYMENT_NOT_CONFIRMED", [x["code"] for x in r["findings"]])
    def test_inventory_shortage_detected(self):
        d = {"orders": [{"order_id": "A", "status": "new", "items": [{"sku": "X", "quantity": 4}]}], "inventory": [{"sku": "X", "available": 2}]}
        self.assertIn("INVENTORY_SHORTAGE", [x["code"] for x in analyze(d)["findings"]])
    def test_carrier_exception_detected(self):
        d = {"orders": [{"order_id": "A", "status": "shipped"}], "shipments": [{"order_id": "A", "carrier_status": "exception"}]}
        self.assertIn("CARRIER_EXCEPTION", [x["code"] for x in analyze(d)["findings"]])
    def test_stale_transit_needs_reference_time(self):
        d = {"config": {"reference_time": "2026-10-15T12:00:00Z", "in_transit_delay_hours": 24}, "orders": [{"order_id": "A", "status": "shipped"}], "shipments": [{"order_id": "A", "carrier_status": "in_transit", "last_event_at": "2026-10-13T12:00:00Z"}]}
        self.assertIn("STALE_IN_TRANSIT", [x["code"] for x in analyze(d)["findings"]])
    def test_cancelled_order_with_active_shipment(self):
        d = {"orders": [{"order_id": "A", "status": "cancelled"}], "shipments": [{"order_id": "A", "carrier_status": "in_transit"}]}
        self.assertIn("CANCELLED_ORDER_HAS_SHIPMENT", [x["code"] for x in analyze(d)["findings"]])
    def test_duplicate_order_id(self):
        self.assertIn("DUPLICATE_ORDER_ID", [x["code"] for x in validate_data({"orders": [{"order_id": "A", "status": "x"}, {"order_id": "A", "status": "x"}]})])
    def test_missing_order_id(self):
        self.assertIn("MISSING_ORDER_ID", [x["code"] for x in validate_data({"orders": [{"status": "new"}]})])
    def test_no_exceptions_status(self):
        r = analyze({"orders": [{"order_id": "A", "status": "processing", "payment_status": "paid"}]})
        self.assertEqual(r["status"], "no_exceptions_detected")
    def test_invalid_root(self):
        self.assertEqual(analyze([])["status"], "invalid_input")

if __name__ == "__main__": unittest.main()
