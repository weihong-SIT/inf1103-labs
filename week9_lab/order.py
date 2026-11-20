from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount


class Order:

    def __init__(
        self,
        order_id: str,
        discount: DiscountStrategy | None = None
    ) -> None:
        self.__order_id = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = (
            discount if discount is not None else NoDiscount()
        )

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(
        self,
        product: Product,
        quantity: int
    ) -> None:

        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, index: int) -> bool:

        if index < 0 or index >= len(self.__order_lines):
            return False

        self.__order_lines.pop(index)
        return True

    def calculate_subtotal(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        # No if/elif here: the strategy decides how the discount works.
        return self.__discount.apply(self.calculate_subtotal())

    def display_order(self) -> None:

        print(f"\nOrder ID: {self.__order_id}")

        if not self.__order_lines:
            print("No order lines.")
            return

        for order_line in self.__order_lines:
            order_line.display_information()

        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Order Total: ${self.calculate_total():.2f}")
