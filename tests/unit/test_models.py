from app.models import User
import pytest
# from factories import (
#     UserFactory,
#     ProductCategoryFactory,
#     ProductFactory,
#     OrderFactory,
#     OrderItemFactory
# )
def test_new_user(app, database):
	"""
		GIVEN a User model
    WHEN a new User is created
    THEN check the fields are defined correctly
	"""
	user = User(
		first_name="Son",
		last_name="Goku",
		address="East District 439",
		zip_code="1000-250",
		location="Mount Paozu",
		vat_number="500123000",
		phone="123456789",
		email="namek420@capsulecorp.com"
	)
	database.session.add(user)
	database.session.commit()

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
