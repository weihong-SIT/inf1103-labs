
from product import Product
from supplier import Supplier


class DigitalProduct(Product):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        download_size: float,
        supplier: Supplier
    ) -> None:

        super().__init__(
            product_id,
            name,
            price,
            stock,
            supplier
        )

        self.__download_size = float(download_size)

        if self.__download_size < 0:
            raise ValueError("Download size cannot be negative")

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def get_type(self) -> str:
        return "digital"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["download_size"] = self.__download_size
        return data
