import json
from pathlib import Path
from product import Product


class Inventory:
    """Manages a collection of Product objects and JSON persistence."""

    def __init__(self, filename="inventory.json"):
        self.__products = []
        self.__filename = Path(filename)
        self.load_inventory()

    def add_product(self, product: Product):
        if self.search_product(product.product_id) is not None:
            raise ValueError("A product with that ID already exists.")
        self.__products.append(product)

    def search_product(self, product_id: str):
        """Find and return a product by ID, or None if it does not exist."""
        product_id = product_id.strip()
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return

        print("\n--- Inventory ---")
        for product in self.__products:
            product.display_information()

    def update_product_stock(self, product_id: str, quantity: int):
        product = self.search_product(product_id)
        if product is None:
            return False
        product.update_stock(quantity)
        return True

    def save_inventory(self):
        """Save all Product objects to JSON."""
        data = [product.to_dict() for product in self.__products]
        try:
            self.__filename.parent.mkdir(parents=True, exist_ok=True)
            temporary_file = self.__filename.with_suffix(self.__filename.suffix + ".tmp")
            with temporary_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            temporary_file.replace(self.__filename)
            print(f"Inventory saved to {self.__filename}.")
        except OSError as error:
            print(f"Error saving inventory: {error}")

    def load_inventory(self):
        """Load JSON data and convert each record into a Product object."""
        if not self.__filename.exists():
            self.__products = []
            return

        try:
            with self.__filename.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("The JSON file must contain a list of products.")

            loaded_products = []
            for item in data:
                product = Product.from_dict(item)
                if any(p.product_id.lower() == product.product_id.lower()
                       for p in loaded_products):
                    raise ValueError(f"Duplicate product ID in JSON: {product.product_id}")
                loaded_products.append(product)

            self.__products = loaded_products
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"Could not load inventory from {self.__filename}: {error}")
            print("Starting with an empty inventory.")
            self.__products = []
