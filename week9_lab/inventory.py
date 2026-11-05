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

    # Add a product
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
    