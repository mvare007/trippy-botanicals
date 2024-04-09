from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Optional
import sqlalchemy as sql
from app import db
from app.models import User

class Validations:
    @staticmethod
    def uniqueness_check(self, field, model):
        if db.session.scalar(sql.select(model).where(
                model == field.data)) is not None:
                raise ValidationError(f'Please use a different {field}.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(9)])
    address = StringField('Address', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(8)])
    location = StringField('Location', validators=[DataRequired()])
    vat_number = StringField('VAT Number', validators=[Length(9)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        Validations.uniqueness_check(self, email, User)

    def validate_vat_number(self, vat_number):
        Validations.uniqueness_check(self, vat_number, User)


