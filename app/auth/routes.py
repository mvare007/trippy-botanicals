from flask import render_template, redirect, url_for, flash, request
from app.auth import bp
import sqlalchemy as sql
from app.extensions import db
from urllib.parse import urlsplit
from app.models.user import User
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sql.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        user.set_last_login()
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                address=form.address.data,
                zip_code=form.zip_code.data,
                location=form.location.data,
                vat_number=form.vat_number.data,
                phone=form.phone.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        except AssertionError as e:
            db.session.rollback()
            flash(f"Error: {e}", "danger")
            return render_template("auth/register.html", title="Register", form=form)

        flash("Registered successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", title="Register", form=form)
