
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from can_be_shipped import CanBeShipped


def test_lab8_relationships():

    print("\n===== ASSOCIATION TEST =====")

    supplier = Supplier(
        "S001",
        "Tech Supplier",
        "supplier@email.com"
    )

    product = PhysicalProduct(
        "P001",
        "Keyboard",
        100.0,
        10,
        1.5,
        supplier
    )

    # Product references Supplier
    print(product.supplier.name)

    # Supplier still exists independently
    del supplier
    print(product.supplier.name)


    print("\n===== AGGREGATION TEST =====")

    inventory = Inventory("test_inventory.json")

    inventory.add_product(product)

    print(inventory.find_product("P001").name)

    # Remove product from Inventory
    inventory.remove_product("P001")

    # Product still exists independently
    print(product.name)


    print("\n===== COMPOSITION TEST =====")

    order = Order("O001")

    order.add_order_line(product, 2)

    print("Order Total:", order.calculate_total())

    # OrderLine references the same Product
    print(order.order_lines[0].product.name)


    print("\n===== INHERITANCE / POLYMORPHISM TEST =====")

    digital_supplier = Supplier(
        "S002",
        "Digital Supplier",
        "digital@email.com"
    )

    digital_product = DigitalProduct(
        "P002",
        "Software",
        50.0,
        100,
        2.5,
        digital_supplier
    )

    products = [product, digital_product]

    for item in products:
        print(item.get_type())
        print(item.get_fulfilment_info())


    print("\n===== LSP TEST =====")

    for item in products:

        # Both subclasses can be treated as Product
        print(item.name)
        print(item.price)
        item.update_stock(1)

    # PhysicalProduct can be treated as CanBeShipped
    if isinstance(product, CanBeShipped):
        print(
            "Shipping Cost:",
            product.calculate_shipping_cost()
        )


if __name__ == "__main__":
    test_lab8_relationships()
