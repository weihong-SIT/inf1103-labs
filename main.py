from inventory import Inventory
from product import Product


def get_non_empty_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def get_price():
    while True:
        try:
            price = float(input("Enter product price: $"))
            if price < 0:
                print("Price cannot be negative.")
                continue
            return price
        except ValueError:
            print("Please enter a valid number, such as 25.50.")


def get_stock(prompt="Enter stock quantity: "):
    while True:
        try:
            stock = int(input(prompt))
            if stock < 0:
                print("Stock cannot be negative.")
                continue
            return stock
        except ValueError:
            print("Please enter a whole number.")


def display_menu():
    print("\n===== Inventory Management System =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")


def main():
    inventory = Inventory("inventory.json")

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            product_id = get_non_empty_text("Enter product ID: ")
            if inventory.search_product(product_id) is not None:
                print("A product with that ID already exists.")
                continue

            name = get_non_empty_text("Enter product name: ")
            price = get_price()
            stock = get_stock()

            try:
                product = Product(product_id, name, price, stock)
                inventory.add_product(product)
                print("Product added successfully.")
            except ValueError as error:
                print(f"Could not add product: {error}")

        elif choice == "3":
            product_id = get_non_empty_text("Enter product ID to update: ")
            product = inventory.search_product(product_id)

            if product is None:
                print("Product not found.")
            else:
                print(f"Current stock for {product.name}: {product.stock}")
                new_stock = get_stock("Enter new stock quantity: ")
                inventory.update_product_stock(product_id, new_stock)
                print("Stock updated successfully.")

        elif choice == "4":
            product_id = get_non_empty_text("Enter product ID to search: ")
            product = inventory.search_product(product_id)

            if product is None:
                print("Product not found.")
            else:
                print("\nProduct found:")
                product.display_information()

        elif choice == "5":
            inventory.save_inventory()

        elif choice == "6":
            inventory.save_inventory()
            print("Exiting Inventory Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
