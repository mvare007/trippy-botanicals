from factory import alchemy, Sequence, SubFactory, Faker
from app.models import User, ProductCategory, Product, Order, OrderItem
from random import randint
from app import db


class UserFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    first_name = Faker.first_name()
    last_name = Faker.last_name()
    address = Faker.street_address()
    zip_code = str(randint(1000, 9999)) + "-" + str(randint(100, 999))
    location = Faker.city()
    vat_number = randint(100000000, 999999999)
    phone = Faker.phone_number()
    email = Sequence(lambda n: f"{n}{Faker.email()}")
    password_hash = Faker.password(length=12)


class ProductCategoryFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ProductCategory
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = Faker.word()
    description = Faker.sentence()


class ProductFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = Faker.word()
    description = Faker.sentence()
    price = randint(100, 9999)
    stock = randint(0, 100)
    category = SubFactory(ProductCategoryFactory)


class OrderFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    user = SubFactory(UserFactory)
    status = Faker.random_element(
        elements=("created", "paid", "shipped", "delivered", "canceled")
    )


class OrderItemFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = OrderItem
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    product = SubFactory(ProductFactory)
    quantity = randint(1, 10)
    order = SubFactory(OrderFactory)
