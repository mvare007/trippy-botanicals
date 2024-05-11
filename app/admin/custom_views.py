from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
import flask_login as login
from flask import flash, redirect, url_for


class AdminModelView(ModelView):
    """This class is used to protect flask admin views from unauthorized access."""

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.admin


class DashboardView(AdminIndexView):
    """This class is used to protect from unauthorized access to the dashboard view."""

    def _handle_view(self, name, **kwargs):
        if not login.current_user.is_authenticated or not login.current_user.admin:
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("main.index"))
        super(DashboardView, self)._handle_view(name, **kwargs)
