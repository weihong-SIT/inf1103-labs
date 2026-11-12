
from product import Product
from order_line import OrderLine


class Order:

    def __init__(self, order_id: str) -> None:
        self.__order_id = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()

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

    def calculate_total(self) -> float:

        total = 0.0

        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()

        return total

    def display_order(self) -> None:

        print(f"\nOrder ID: {self.__order_id}")

        if not self.__order_lines:
            print("No order lines.")
            return

        for order_line in self.__order_lines:
            order_line.display_information()

        print(f"Order Total: ${self.calculate_total():.2f}")
