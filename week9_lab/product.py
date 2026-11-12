
from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ) -> None:

        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = int(stock)
        self.__supplier = supplier

        if self.__price < 0 or self.__stock < 0:
            raise ValueError("Price and stock cannot be negative")

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:

        quantity = int(quantity)

        if quantity < 0:
            raise ValueError("Stock cannot be negative")

        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def display_supplier(self) -> None:
        self.__supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "type": self.get_type(),
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": {
                "supplier_id": self.__supplier.supplier_id,
                "name": self.__supplier.name,
                "contact_email": self.__supplier.contact_email
            }
        }

