import json

# ----------------------------------------
# Load inventory from JSON file
# ----------------------------------------
def load_inventory():

    try:
        with open("inventory.json", "r") as file:
            inventory = json.load(file)

        print("inventory.json found.")
        print("Inventory loaded successfully.")

        return inventory

    except FileNotFoundError:
        print("inventory.json not found.")
        print("Starting with an empty inventory.")

        return []


# ----------------------------------------
# Save inventory to JSON file
# ----------------------------------------
def save_inventory(inventory):

    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully.")

# ----------------------------------------
# Display all products
# ----------------------------------------
def display_all(inventory):
    print("\nCurrent Inventory")
    print("---------------------------------------------")

    if len(inventory) == 0:
        print("Inventory is empty.")
    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | "
                f"Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )

    print("---------------------------------------------")


# ----------------------------------------
# Add a new product
# ----------------------------------------
def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(product)

    print("\nProduct added successfully!")


# ----------------------------------------
# Update product stock
# ----------------------------------------
def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ")

    for product in inventory:
        if product["id"] == product_id:
            print(f"Current stock: {product['stock']}")

            new_stock = int(input("Enter new stock quantity: "))

            product["stock"] = new_stock

            print("Stock updated successfully!")
            return

    print("Product not found.")


# ----------------------------------------
# Search for a product
# ----------------------------------------
def search_product(inventory):
    print("\nSearch Product")

    search_id = input("Enter Product ID: ")

    for product in inventory:
        if product["id"] == search_id:
            print("\nProduct Found")
            print("---------------------------------------------")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("---------------------------------------------")
            return

    print("Product not found.")


# ----------------------------------------
# Main program
# ----------------------------------------

print("==========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("==========================================")

inventory = load_inventory()


while True:

    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")

    option = input("Enter option: ")

    if option == "1":
        display_all(inventory)

    elif option == "2":
        add_product(inventory)

    elif option == "3":
        update_stock(inventory)

    elif option == "4":
        search_product(inventory)

    elif option == "5":
        save_inventory(inventory)

    elif option == "6":
        print("Exiting program...")
        break

    else:
        print("Invalid option. Please try again.")