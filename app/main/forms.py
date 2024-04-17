import sqlalchemy as sql
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

from app import db
from app.models import User


class CheckoutForm(FlaskForm):
    card_number = StringField("Card Number", validators=[DataRequired()])
    cvv = StringField("CVV", validators=[DataRequired()])
    expiration_date = StringField("Expiration Date", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    zip_code = StringField("Zip Code", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    vat_number = StringField("VAT", validators=[Optional()])
    terms_and_conditions = BooleanField(
        "I agree to the terms and conditions", validators=[DataRequired()]
    )
    submit = SubmitField("Place Order")
