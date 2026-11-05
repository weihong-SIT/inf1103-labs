
from abc import ABC, abstractmethod


class Product(ABC):

    def __init__(self, product_id, name, price, stock):
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = int(stock)

        if self.__price < 0 or self.__stock < 0:
            raise ValueError("Price and stock cannot be negative")

    # Properties for accessing private attributes
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        quantity = int(quantity)

        if quantity < 0:
            raise ValueError("Stock cannot be negative")

        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    # Abstract methods
    @abstractmethod
    def get_fulfilment_info(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    # Convert product information into a dictionary
    def to_dict(self):
        return {
            "type": self.get_type(),
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }
