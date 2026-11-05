import json
from pathlib import Path

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class Inventory:

    def __init__(self, filename="inventory.json"):
        self.__products = []
        self.__filename = Path(filename)

        self.load_inventory()

    
    def add_product(self, product):

        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added")

        if self.search_product(product.product_id):
            raise ValueError("Product ID already exists")

        self.__products.append(product)

    def search_product(self, product_id):

        for product in self.__products:

            if product.product_id.lower() == str(product_id).strip().lower():
                return product

        return None
     def display_all(self):

        if not self.__products:
            print("Inventory is empty.")
            return

        for product in self.__products:

            product.display_information()

            print("Fulfilment:", product.get_fulfilment_info())
            print()

    
    def update_product_stock(self, product_id, quantity):

        product = self.search_product(product_id)

        if product is None:
            return False

        product.update_stock(quantity)

        return True
     def save_inventory(self):

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

    # Load inventory from JSON
    def load_inventory(self):

        if not self.__filename.exists():
            self.__products = []
            return

        try:

            with self.__filename.open(encoding="utf-8") as file:
                records = json.load(file)

            products = []

            for item in records:

                if item["type"] == "physical":

                    product = PhysicalProduct(
                        item["product_id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["weight"]
                    )

                elif item["type"] == "digital":

                    product = DigitalProduct(
                        item["product_id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["download_size"]
                    )

                else:
                    raise ValueError(
                        "Unknown product type: " + str(item.get("type"))
                    )

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
