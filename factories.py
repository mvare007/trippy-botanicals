from factory import alchemy, Sequence, SubFactory, Faker, LazyAttribute, post_generation
from app.models.user import User
from app.models.product_category import ProductCategory
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from random import randint
from app.extensions import db


class UserFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    address = Faker("street_address")
    zip_code = str(randint(1000, 9999)) + "-" + str(randint(100, 999))
    location = Faker("city")
    vat_number = str(randint(100000000, 123456789))
    phone = Faker("phone_number")
    email = Sequence(lambda n: "user{}@demo.com".format(n))

    @post_generation
    def set_password(obj, create, _extracted, **kwargs):
        if not create:
            return

        password = User.generate_password()
        obj.set_password(password)


class ProductCategoryFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ProductCategory
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = Sequence(lambda n: "product category {}".format(n))
    description = Faker("sentence")


class ProductFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = Sequence(lambda n: "product {}".format(n))
    description = Faker("sentence")
    price = randint(100, 9999)
    stock = randint(0, 100)
    category = SubFactory(ProductCategoryFactory)


class OrderFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    user = SubFactory(UserFactory)
    status = Faker(
        "random_element",
        elements=("Created", "Processed", "Shipped", "Delivered", "Cancelled"),
    )


class OrderItemFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = OrderItem
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    product = SubFactory(ProductFactory)
    quantity = randint(1, 10)
    order = SubFactory(OrderFactory)
