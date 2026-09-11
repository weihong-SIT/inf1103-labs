
inventory = 0
failedattempt = 0
excess = 0
user_input = ""

while user_input.lower() != "quit":
    stock = input("Enter stock quantity: ")
    if stock.isdigit():
        inventory = inventory + int(stock)
        if inventory > 500:
            print("exceeded inventory limit")
            user_input = "quit"
        else:
            inventory = inventory
    elif stock == "quit":
        user_input = stock
    else:
        print("invalid data, please enter again.")
        failedattempt = failedattempt + 1
if inventory <= 500:
    print("Inventory: ", inventory)
else:
    excess = inventory - 500
    inventory = 500
    print("inventory", inventory)
    print("excess: ", excess)
print("failed attempt: ", failedattempt)