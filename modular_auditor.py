def get_valid_input():
    inventory = 0
    failedattempt = 0
    user_input = ""
    while user_input.lower() != "quit":
        stock = input("Enter stock quantity: ")
        if stock.isdigit():
            inventory = inventory + int(stock)
        elif stock == "quit":
            user_input = stock
        else:
            print("invalid data, please enter again.")
            failedattempt = failedattempt + 1
    return inventory, failedattempt
inventory = get_valid_input()
print("inventory", inventory)
    
