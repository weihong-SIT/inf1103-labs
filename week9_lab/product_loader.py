import csv

from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file through ProductFactory.

    The lab CSV has 5 columns:
        product_type,product_id,name,price,stock_quantity
    It has no weight / download-size column, so an optional 6th column is
    used if present; otherwise 0.0 is used.
    """

    loaded = 0

    try:
        file = open(path, newline="")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        with file:

            reader = csv.reader(file)
            next(reader, None)  # skip the header row

            for row_number, row in enumerate(reader, start=2):

                try:
                    if len(row) < 5:
                        raise ValueError("expected at least 5 columns")

                    product_type, product_id, name, price, stock = row[:5]
                    extra = row[5] if len(row) > 5 else 0.0

                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        price,
                        stock,
                        extra,
                        supplier
                    )

                    inventory.add_product(product)
                    loaded += 1

                except ValueError as error:
                    print(f"Row {row_number} skipped: {error}")

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")