import unittest

from digital_product import DigitalProduct
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("S1", "Sup", "s@x.com")


class TestFactory(unittest.TestCase):

    def test_factory_builds_physical_product(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, 1.5, SUPPLIER)
        self.assertIsInstance(p, PhysicalProduct)
        self.assertIsInstance(p, Product)

    def test_factory_builds_digital_product(self):
        p = ProductFactory.create("digital", "D1", "App", 49.9, 100, 20.0, SUPPLIER)
        self.assertIsInstance(p, DigitalProduct)
        self.assertIsInstance(p, Product)

    def test_unknown_product_type_raises_clear_error(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S1", "Install", 30.0, 5, 0, SUPPLIER)


class TestValidation(unittest.TestCase):

    def test_invalid_price_rejected(self):
        for price in (0, -1, -0.01):
            with self.subTest(price=price):
                with self.assertRaisesRegex(ValueError, "Price must be greater than zero"):
                    ProductFactory.create("physical", "P1", "Lamp", price, 1, 1.0, SUPPLIER)

    def test_negative_stock_rejected(self):
        with self.assertRaisesRegex(ValueError, "Stock quantity cannot be negative"):
            ProductFactory.create("digital", "D1", "App", 10.0, -1, 1.0, SUPPLIER)

    def test_update_stock_negative_rejected_for_every_subclass(self):
        for kind in ("physical", "digital"):
            with self.subTest(kind=kind):
                p = ProductFactory.create(kind, "X", "Thing", 10.0, 1, 1.0, SUPPLIER)
                with self.assertRaises(ValueError):
                    p.update_stock(-5)

    def test_order_line_quantity_rejected(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, 1.0, SUPPLIER)
        for quantity in (0, -3):
            with self.subTest(quantity=quantity):
                with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero"):
                    OrderLine(p, quantity)


if __name__ == "__main__":
    unittest.main()
