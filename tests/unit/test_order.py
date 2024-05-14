import pytest
from factories import OrderFactory, OrderItemFactory, ProductFactory


def test_order_total(database):
    # GIVEN an order with items
    order = create_order_with_items(database)

    # WHEN we calculate the total
    total = order.total()

    # THEN the total should be the sum of the quantity times the product price of each item
    assert total == 100


def test_order_tax_total(database):
    # GIVEN an order with items
    order = create_order_with_items(database)

    # WHEN we calculate the tax total
    tax_total = order.tax_total()

    # THEN the tax total should be the total times the tax rate
    assert tax_total == 23


def test_order_net_total(database):
    # GIVEN an order with items
    order = create_order_with_items(database)

    # WHEN we calculate the net total
    net_total = order.net_total()

    # THEN the net total should be the total plus the tax total
    assert net_total == 123


def create_order_with_items(database):
    order = OrderFactory()
    product = ProductFactory.create(price=10)
    order_items = OrderItemFactory.create_batch(5, order=order, quantity=2)
    for item in order_items:
        item.product = product
        database.session.add(item)
    database.session.add(order)
    database.session.add(product)
    database.session.commit()

    return order
