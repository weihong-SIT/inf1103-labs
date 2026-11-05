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
