import ast
import inspect
import textwrap
import unittest

from discount_strategy import (
    DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount,
    StudentDiscount,
)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class TestDiscountStrategies(unittest.TestCase):

    def setUp(self):
        self.product = ProductFactory.create(
            "physical", "P1", "Item", 50.0, 10, 1.0,
            Supplier("S1", "Sup", "s@x.com")
        )

    def make_order(self, discount=None):
        order = Order("O1", discount)
        order.add_order_line(self.product, 5)  # 5 x 50 = 250
        return order

    def test_default_is_no_discount(self):
        self.assertEqual(self.make_order().calculate_total(), 250)

    def test_bulk_discount_applies_over_threshold(self):
        order = self.make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

    def test_bulk_discount_not_applied_under_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_set_discount_changes_strategy(self):
        order = self.make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_new_strategy_works_without_changing_order(self):
        order = self.make_order(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_strategies_share_base_class(self):
        for cls in (NoDiscount, PercentageDiscount, BulkDiscount,
                    StudentDiscount):
            self.assertTrue(issubclass(cls, DiscountStrategy))

    def test_order_has_no_discount_if_elif_logic(self):
        # calculate_total / set_discount must contain no if/elif at all.
        for method in (Order.calculate_total, Order.set_discount):
            tree = ast.parse(textwrap.dedent(inspect.getsource(method)))
            conditionals = [
                n for n in ast.walk(tree) if isinstance(n, (ast.If, ast.IfExp))
            ]
            self.assertEqual(conditionals, [], method.__name__)

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)


if __name__ == "__main__":
    unittest.main()
