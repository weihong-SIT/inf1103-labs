def load_inventory():
    orders = []
    try:
        with open("order.txt", "r") as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()

                if line:
                    parts = line.split(",")

                    orders_id = parts[0].strip()
                    product_name = parts[1].strip()
                    quantity = parts[2].strip()

                    orders.append([orders_id, product_name, quantity])
    except FileNotFoundError:
        orders = []
    return orders
def save_inventory(orders):
    order = []
    with open("order.txt", "w") as file:
        for order in orders:
            file.write(",".join(map(str, order)) + "\n")

def get_valid_input():
    orders = load_inventory()
    for order in orders:
        print(order)
    entry = 1000
    if orders:
        entry = int(orders[-1][0])

    while True:
        print()
        new_item = input("Enter the item: ")
        if new_item.lower() == "quit":
            break
        else:
            quantity = input("enter quantity: ")
            entry = entry + 1
            new_entry = [entry, new_item, quantity]
            orders.append(new_entry)
            save_inventory(orders)
            print()
            print("New Order added: ")
            print(new_entry)
        print("order successfuly saved to orders.txt")
print("Current Orders: ")
print()
get_valid_input()
