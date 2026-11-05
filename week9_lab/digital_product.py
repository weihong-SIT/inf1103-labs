
from product import Product


class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)

        self.__download_size = float(download_size)

        if self.__download_size < 0:
            raise ValueError("Download size cannot be negative")

    @property
    def download_size(self):
        return self.__download_size

    # Override parent method
    def display_information(self):
        super().display_information()
        print(f"Download size: {self.__download_size:.2f} MB")

    # Implement abstract method
    def get_fulfilment_info(self):
        return "This product is delivered digitally."

    def get_type(self):
        return "digital"

    # Add download size when converting to dictionary
    def to_dict(self):
        data = super().to_dict()
        data["download_size"] = self.__download_size
        return data
