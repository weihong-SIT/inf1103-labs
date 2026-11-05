
from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)

        self.__weight = float(weight)

        if self.__weight < 0:
            raise ValueError("Weight cannot be negative")

    @property
    def weight(self):
        return self.__weight

    # Override parent method
    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    # Implement abstract method
    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    # Implement CanBeShipped method
    def calculate_shipping_cost(self):
        return 5.00 + (2.00 * self.__weight)

    def get_type(self):
        return "physical"

    # Add weight when converting to dictionary
    def to_dict(self):
        data = super().to_dict()
        data["weight"] = self.__weight
        return data
