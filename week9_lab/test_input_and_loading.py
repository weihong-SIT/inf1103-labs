import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

from input_helper import get_positive_float
from inventory import Inventory
from product_loader import load_products
from supplier import Supplier

CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""
SUPPLIER = Supplier("S1", "Sup", "s@x.com")


def run_captured(func, *args):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):

    def test_asks_again_until_valid(self):
        with mock.patch("builtins.input", side_effect=["abc", "-5", "0", "12.50"]):
            value, out = run_captured(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertIn("Please enter a valid number", out)
        self.assertIn("Please enter a number greater than zero.", out)


class TestLoadProducts(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.inv = Inventory(os.path.join(self.tmp.name, "inv.json"))

    def test_missing_file_handled(self):
        missing = os.path.join(self.tmp.name, "nope.csv")
        _, out = run_captured(load_products, missing, self.inv, SUPPLIER)
        self.assertIn("Products file not found", out)
        self.assertIn("Load attempt finished.", out)
        self.assertNotIn("products loaded", out)
        self.assertEqual(self.inv.products, [])

    def test_bad_rows_skipped_and_good_rows_loaded(self):
        path = os.path.join(self.tmp.name, "products.csv")
        with open(path, "w", newline="") as f:
            f.write(CSV)
        _, out = run_captured(load_products, path, self.inv, SUPPLIER)
        self.assertEqual(
            [p.product_id for p in self.inv.products], ["P001", "D001", "P003"]
        )
        self.assertIn("Row 4 skipped: Unknown product type: service", out)
        self.assertIn("Row 5 skipped", out)
        self.assertIn("3 products loaded.", out)
        self.assertTrue(out.strip().endswith("Load attempt finished."))


if __name__ == "__main__":
    unittest.main()
