from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class ProductFactory:
    """Single place that knows which concrete Product class to build.

    `extra` is the one value that differs between product types:
    weight (kg) for a physical product, download size (MB) for a digital one.
    """

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        extra: float,
        supplier: Supplier
    ) -> Product:

        product_type = str(product_type).strip().lower()

        if product_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, extra, supplier
            )

        elif product_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, extra, supplier
            )

        else:
            raise ValueError(f"Unknown product type: {product_type}")