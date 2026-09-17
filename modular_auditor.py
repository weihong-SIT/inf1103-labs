inventory = 0
failedattempt = 0
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

def general_report(total_units, failedattempt):
    print("Inventory: ", total_units)
    print("failed attempts", failedattempt)
    
def process_delivery(current_total,new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

inventory, failedattempt = get_valid_input()
general_report(inventory, failedattempt)
amount = process_delivery(inventory, 10)
print("tax amount:", calculate_tax(amount))
