from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped

def text_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Cannot be empty.")


def number(prompt, kind=float):
    while True:
        try:
            value = kind(input(prompt))

            if value < 0:
                print("Cannot be negative.")
                continue

            return value

        except ValueError:
            print("Enter a valid number.")


def menu():
    print("\n===== Inventory Management System =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")

def add_product(inventory):

    print("\n1. Physical product")
    print("2. Digital product")

    kind = input("Choose type: ").strip()

    if kind not in ("1", "2"):
        print("Invalid type.")
        return

    product_id = text_input("Product ID: ")

    if inventory.search_product(product_id):
        print("ID already exists.")
        return

    name = text_input("Product name: ")
    price = number("Price ($): ")
    stock = number("Stock: ", int)

    if kind == "1":

        weight = number("Weight (kg): ")

        product = PhysicalProduct(
            product_id,
            name,
            price,
            stock,
            weight
        )

    else:

        download_size = number("Download size (MB): ")

        product = DigitalProduct(
            product_id,
            name,
            price,
            stock,
            download_size
        )

    inventory.add_product(product)

    print("Added:", product.get_fulfilment_info())

    if isinstance(product, CanBeShipped):

        print(
            f"Shipping cost: "
            f"${product.calculate_shipping_cost():.2f}"
        )


# Main program
def main():

    inventory = Inventory("inventory.json")

    while True:

        menu()

        choice = input("Choice (1-6): ").strip()

        if choice == "1":

            inventory.display_all()

        elif choice == "2":

            try:
                add_product(inventory)

            except ValueError as error:
                print("Error:", error)

        elif choice == "3":

            product_id = text_input("Product ID: ")

            product = inventory.search_product(product_id)

            if product is None:
                print("Not found.")

            else:

                quantity = number("New stock: ", int)

                inventory.update_product_stock(
                    product_id,
                    quantity
                )

                print("Stock updated.")

        elif choice == "4":

            product_id = text_input("Product ID: ")

            product = inventory.search_product(product_id)

            if product is None:
                print("Not found.")

            else:

                product.display_information()

                print(product.get_fulfilment_info())

                if isinstance(product, CanBeShipped):

                    print(
                        f"Shipping: "
                        f"${product.calculate_shipping_cost():.2f}"
                    )

        elif choice == "5":

            inventory.save_inventory()

        elif choice == "6":

            inventory.save_inventory()

            print("Goodbye.")

            break

        else:

            print("Choose 1 to 6.")


if __name__ == "__main__":
    main()