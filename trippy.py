import sqlalchemy as sql
import sqlalchemy.orm as orm
from app import create_app, db
from app.models import User, ProductCategory, Product, Order, OrderItem

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "sql": sql,
        "orm": orm,
        "db": db,
        "User": User,
        "ProductCategory": ProductCategory,
        "Product": Product,
        "Order": Order,
        "OrderItem": OrderItem,
    }

# TODO:
# * Authorization (login) X
# * Sql alchemy seed  - user admin and some products X
# * Backoffice page (only available for admin users) with CRUDS for users, product categories, products, and orders
# * handle uploads
# * Feature daily guessing game - wins points for user
# * Shopping cart
# * Service to send order data to shipping company
# * Tests

# TODO: User Stories
# * As a user, I want to be able to register and login X
# * As a user, I want to be able to browse products
# * As a user, I want to be able to add products to my shopping cart
# * As a user, I want to be able to checkout
# * As a user, I want to be able to see my order history
# * As an admin, I want to be able to add products
# * As an admin, I want to be able to see all orders
# * As an admin, I want to be able to see all users
# * As an admin, I want to be able to see all products
# * As an admin, I want to be able to see all product categories

# TODO: AZURE
# * Build container
# * CI/CD
# * Cosmos DB
# * Azure Blob Storage
