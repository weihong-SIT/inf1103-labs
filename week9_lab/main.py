
from inventory import Inventory
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from product import Product
from can_be_shipped import CanBeShipped


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


def add_product(inventory: Inventory) -> None:

    print("\n1. Physical product")
    print("2. Digital product")

    kind = input("Choose type: ").strip()

    if kind not in ("1", "2"):
        print("Invalid type.")
        return

    product_id = text_input("Product ID: ")

    if inventory.find_product(product_id):
        print("ID already exists.")
        return

    name = text_input("Product name: ")
    price = number("Price ($): ")
    stock = number("Stock: ", int)

    print("\nEnter supplier information")

    supplier = Supplier(
        text_input("Supplier ID: "),
        text_input("Supplier name: "),
        text_input("Supplier email: ")
    )

    if kind == "1":

        weight = number("Weight (kg): ")

        product = PhysicalProduct(
            product_id,
            name,
            price,
            stock,
            weight,
            supplier
        )

    else:

        download_size = number("Download size (MB): ")

        product = DigitalProduct(
            product_id,
            name,
            price,
            stock,
            download_size,
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

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            continue

        order.add_order_line(product, quantity)
        print("Product added to order.")

    order.display_order()


def menu() -> None:

    print("\n===== Inventory Management System =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Remove product from inventory")
    print("6. Create an order")
    print("7. Save inventory")
    print("8. Exit")


def main() -> None:

    inventory = Inventory("inventory.json")

    while True:

        menu()
        choice = input("Choice (1-8): ").strip()

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

                inventory.save_inventory()
                print("Goodbye.")
                break

            else:

                print("Choose 1 to 8.")

        except ValueError as error:
            print("Error:", error)
if __name__ == "__main__":
    main()
