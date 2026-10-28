import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from decimal import Decimal
from case_studies.ecommerce.refactored_orders import Cart, OrderItem, DiscountType
from case_studies.etl.refactored_etl import clean_user_records, UserRecord


class TestRefactoredOrders(unittest.TestCase):
    def test_order_calculations_with_save20(self):
        cart = Cart()
        # Item > 100 gets 20% discount
        item = OrderItem("Gaming Monitor", Decimal("200.00"), 1, DiscountType.SAVE20)
        cart.add_item(item)

        self.assertEqual(item.gross_subtotal, Decimal("200.00"))
        self.assertEqual(item.discount_amount, Decimal("40.00"))
        self.assertEqual(item.net_subtotal, Decimal("160.00"))
        self.assertEqual(item.tax_amount, Decimal("13.20")) # 160 * 0.0825
        self.assertEqual(item.total, Decimal("173.20"))

    def test_order_validation(self):
        with self.assertRaises(ValueError):
            OrderItem("", Decimal("50.00"), 1)
        with self.assertRaises(ValueError):
            OrderItem("Valid", Decimal("-10.00"), 1)
        with self.assertRaises(ValueError):
            OrderItem("Valid", Decimal("10.00"), 0)


class TestRefactoredETL(unittest.TestCase):
    def test_deduplication_and_validation(self):
        raw = [
            {"name": "Alice Smith", "email": "alice@example.com", "age": 25},
            {"name": "Alice Duplicate", "email": "alice@example.com", "age": 30},
            {"name": "Underage Kid", "email": "kid@example.com", "age": 12},
            {"name": "Bad Email", "email": "invalid-email-address", "age": 28},
            {"name": "Bob Jones", "email": "bob@example.com", "age": 45}
        ]
        cleaned, dropped = clean_user_records(raw)
        self.assertEqual(len(cleaned), 2) # Only Alice and Bob
        self.assertEqual(dropped, 3)
        self.assertEqual(cleaned[0].email, "alice@example.com")
        self.assertEqual(cleaned[1].email, "bob@example.com")


if __name__ == "__main__":
    unittest.main()
