import pytest
from factories import ProductFactory
from app.models.product import Product


def test_featured_products(database):
    # GIVEN all products
    ProductFactory.create_batch(2, stock=0)
    ProductFactory.create(stock=5)
    ProductFactory.create(stock=10)

    # WHEN fetching featured products with a given count
    products = Product.featured(4)

    # THEN return that count of products ordered by stock in descending order
    assert len(products) == 4
    assert products[0].stock == 10
    assert products[1].stock == 5
    assert products[2].stock == 0
    assert products[3].stock == 0


def test_product_is_available(database):
    # GIVEN a product with stock and another without stock
    available_product = ProductFactory.create(stock=5)
    unavailable_product = ProductFactory.create(stock=0)

    # WHEN checking if the product is available
    available = available_product.is_available()
    unavailable = unavailable_product.is_available()

    # THEN return True if stock is greater than 0
    assert available == True
    assert unavailable == False
