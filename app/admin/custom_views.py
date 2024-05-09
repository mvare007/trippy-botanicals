from flask_admin import AdminIndexView
from flask_login import login_required
from flask_admin.contrib.sqla import ModelView
import flask_login as login

class AdminModelView(ModelView):
    """This class is used to protect flask admin views from unauthorized access."""
    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.admin


class DashboardView(AdminIndexView):
    """This class is used to protect from unauthorized access to the dashboard view."""
    @login_required
    def _handle_view(self, name, **kwargs):
        super(DashboardView, self)._handle_view(name, **kwargs)