import pytest
from app.models.user import User
from factories import UserFactory, OrderFactory


def test_new_user(database):
    # GIVEN a User model
    user = User(
        first_name="Son",
        last_name="Goku",
        address="East District 439",
        zip_code="1000-250",
        location="Mount Paozu",
        vat_number="500123000",
        phone="123456789",
        email="namek420@capsulecorp.com",
    )

    # WHEN a new User is created
    database.session.add(user)
    database.session.commit()

    # THEN check the fields are defined correctly
    assert user.id is not None
    assert user.first_name == "Son"
    assert user.last_name == "Goku"
    assert user.address == "East District 439"
    assert user.zip_code == "1000-250"
    assert user.location == "Mount Paozu"
    assert user.vat_number == "500123000"
    assert user.phone == "123456789"
    assert user.email == "namek420@capsulecorp.com"
    assert user.admin is False
    assert user.date_joined is not None
    assert user.created_at is not None
    assert user.last_login is None


def test_current_order(database):
    # GIVEN a User model
    user = UserFactory()
    database.session.add(user)

    # WHEN a user has a order with 'Pending' status
    order = OrderFactory(user=user, status="Pending")
    database.session.add(order)

    database.session.commit()

    # THEN check the current_order property
    assert user.current_order().id == order.id


def test_current_order_no_order(database):
    """
    GIVEN a User model
    WHEN a user has no orders
    THEN check the current_order property
    """
    user = UserFactory()
    database.session.add(user)
    database.session.commit()

    assert user.current_order() is None


def test_user_full_name(database):
    # GIVEN a User model
    user = UserFactory()

    # WHEN we call the full_name property
    full_name = user.full_name()

    # THEN check the full_name property
    assert full_name == f"{user.first_name} {user.last_name}"


def test_user_set_last_login(database):
    # GIVEN a User model
    user = UserFactory(last_login=None)

    # WHEN we call the set_last_login method
    user.set_last_login()

    # THEN check the last_login property is set
    assert user.last_login is not None
