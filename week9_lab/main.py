
from inventory import Inventory
from supplier import Supplier
from order import Order
from product import Product
from can_be_shipped import CanBeShipped
from product_factory import ProductFactory
from input_helper import get_positive_float
from product_loader import load_products
from discount_strategy import (
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)


def text_input(prompt: str) -> str:

    while True:

        value = input(prompt).strip()

        if value:
            return value

        print("Cannot be empty.")


def number(prompt: str, kind=float):

    while True:

        try:

            value = kind(input(prompt))

            if value < 0:
                print("Cannot be negative.")
                continue

            return value

        except ValueError:
            print("Enter a valid number.")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def ask_supplier() -> Supplier:

    print("\nEnter supplier information")

    return Supplier(
        text_input("Supplier ID: "),
        text_input("Supplier name: "),
        text_input("Supplier email: ")
    )


def add_product(inventory: Inventory) -> None:

    print("\n1. Physical product")
    print("2. Digital product")

    product_types = {"1": "physical", "2": "digital"}
    extra_prompts = {
        "physical": "Weight (kg): ",
        "digital": "Download size (MB): "
    }

    choice = input("Choose type: ").strip()

    if choice not in product_types:
        print("Invalid type.")
        return

    product_type = product_types[choice]

    product_id = text_input("Product ID: ")

    if inventory.find_product(product_id):
        print("ID already exists.")
        return

    name = text_input("Product name: ")
    price = get_positive_float("Price ($): ")
    stock = number("Stock: ", int)
    supplier = ask_supplier()
    extra = number(extra_prompts[product_type])

    # The factory decides which concrete class to build.
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

    print("\nProduct added successfully.")
    print("Supplier information:")
    product.display_supplier()

    if isinstance(product, CanBeShipped):
        print(
            f"Shipping cost: "
            f"${product.calculate_shipping_cost():.2f}"
        )


def search_product(inventory: Inventory) -> None:

    product_id = text_input("Product ID: ")
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    show_product_details(product)

    print("\nSupplier:")
    product.display_supplier()

    if isinstance(product, CanBeShipped):
        print(
            f"Shipping cost: "
            f"${product.calculate_shipping_cost():.2f}"
        )


def update_stock(inventory: Inventory) -> None:

    product_id = text_input("Product ID: ")

    if inventory.find_product(product_id) is None:
        print("Product not found.")
        return

    quantity = number("New stock: ", int)

    inventory.update_product_stock(product_id, quantity)
    print("Stock updated.")


def choose_discount() -> DiscountStrategy:

    print("\nDiscount options")
    print("1. No discount")
    print("2. Percentage discount")
    print("3. Bulk discount")
    print("4. Student discount (5%)")

    while True:

        choice = input("Choose discount (1-4): ").strip()

        try:

            if choice == "1":
                return NoDiscount()

            elif choice == "2":
                return PercentageDiscount(
                    get_positive_float("Percentage off (e.g. 10): ")
                )

            elif choice == "3":
                threshold = get_positive_float("Order total threshold: ")
                amount = get_positive_float("Amount off: ")
                return BulkDiscount(threshold, amount)

            elif choice == "4":
                return StudentDiscount()

            else:
                print("Choose 1 to 4.")

        except ValueError as error:
            print("Error:", error)


def create_order(inventory: Inventory) -> None:

    order = Order(text_input("Order ID: "))

    while True:

        product_id = input(
            "Product ID (or 'done' to finish): "
        ).strip()

        if product_id.lower() == "done":
            break

        product = inventory.find_product(product_id)

        if product is None:
            print("Product not found.")
            continue

        quantity = number("Quantity: ", int)

        try:
            order.add_order_line(product, quantity)
            print("Product added to order.")
        except ValueError as error:
            print("Error:", error)

    order.set_discount(choose_discount())
    order.display_order()


def import_products(inventory: Inventory) -> None:

    path = input("CSV file path [products.csv]: ").strip() or "products.csv"
    supplier = ask_supplier()
    load_products(path, inventory, supplier)


def menu() -> None:

    print("\n===== Inventory Management System =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Remove product from inventory")
    print("6. Create an order")
    print("7. Save inventory")
    print("8. Load products from CSV")
    print("9. Exit")


def main() -> None:

    inventory = Inventory("inventory.json")

    while True:

        menu()
        choice = input("Choice (1-9): ").strip()

        try:

            if choice == "1":

                inventory.display_all_products()

            elif choice == "2":

                add_product(inventory)

            elif choice == "3":

                update_stock(inventory)

            elif choice == "4":

                search_product(inventory)

            elif choice == "5":

                product_id = text_input("Product ID: ")

                if inventory.remove_product(product_id):
                    print("Product removed from inventory.")
                else:
                    print("Product not found.")

            elif choice == "6":

                create_order(inventory)

            elif choice == "7":

                inventory.save_inventory()

            elif choice == "8":

                import_products(inventory)

            elif choice == "9":

                inventory.save_inventory()
                print("Goodbye.")
                break

            else:

                print("Choose 1 to 9.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
