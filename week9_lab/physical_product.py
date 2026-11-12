
from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        weight: float,
        supplier: Supplier
    ) -> None:

        super().__init__(
            product_id,
            name,
            price,
            stock,
            supplier
        )

        self.__weight = float(weight)

        if self.__weight < 0:
            raise ValueError("Weight cannot be negative")

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (2.00 * self.__weight)

    def get_type(self) -> str:
        return "physical"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["weight"] = self.__weight
        return data
