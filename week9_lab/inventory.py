
import json
from pathlib import Path

from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class Inventory:

    def __init__(self, filename: str = "inventory.json") -> None:
        self.__products: list[Product] = []
        self.__filename = Path(filename)
        self.load_inventory()

    @property
    def products(self) -> list[Product]:
        return self.__products.copy()

    def add_product(self, product: Product) -> None:

        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added")

        if self.find_product(product.product_id):
            raise ValueError("Product ID already exists")

        self.__products.append(product)

    def remove_product(self, product_id: str) -> bool:

        product = self.find_product(product_id)

        if product is None:
            return False

        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:

        for product in self.__products:

            if product.product_id.lower() == str(
                product_id
            ).strip().lower():

                return product

        return None

    # Compatibility with Lab 7
    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def display_all_products(self) -> None:

        if not self.__products:
            print("Inventory is empty.")
            return

        for product in self.__products:
            product.display_information()
            print("Fulfilment:", product.get_fulfilment_info())
            print()

    # Compatibility with Lab 7
    def display_all(self) -> None:
        self.display_all_products()

    def update_product_stock(
        self,
        product_id: str,
        quantity: int
    ) -> bool:

        product = self.find_product(product_id)

        if product is None:
            return False

        product.update_stock(quantity)
        return True

    def save_inventory(self) -> None:

        try:

            self.__filename.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            temporary = self.__filename.with_suffix(
                self.__filename.suffix + ".tmp"
            )

            with temporary.open("w", encoding="utf-8") as file:

                json.dump(
                    [product.to_dict() for product in self.__products],
                    file,
                    indent=4
                )

            temporary.replace(self.__filename)
            print("Inventory saved.")

        except OSError as error:
            print("Save error:", error)

    def load_inventory(self) -> None:

        if not self.__filename.exists():
            self.__products = []
            return

        try:

            with self.__filename.open(encoding="utf-8") as file:
                records = json.load(file)

            products: list[Product] = []

            for item in records:

                # Support older Lab 7 JSON files
                supplier_data = item.get(
                    "supplier",
                    {
                        "supplier_id": "UNKNOWN",
                        "name": "Unknown Supplier",
                        "contact_email": "unknown@example.com"
                    }
                )

                supplier = Supplier(
                    supplier_data["supplier_id"],
                    supplier_data["name"],
                    supplier_data["contact_email"]
                )

                if item["type"] == "physical":

                    product = PhysicalProduct(
                        item["product_id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["weight"],
                        supplier
                    )

                elif item["type"] == "digital":

                    product = DigitalProduct(
                        item["product_id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["download_size"],
                        supplier
                    )

                else:
                    raise ValueError("Unknown product type")

                if any(
                    p.product_id.lower() == product.product_id.lower()
                    for p in products
                ):
                    raise ValueError("Duplicate product ID")

                products.append(product)

            self.__products = products

        except (
            OSError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError
        ) as error:

            print("Could not load inventory:", error)
            self.__products = []
