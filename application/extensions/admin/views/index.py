from flask_admin import AdminIndexView

from application.extensions.auth import login_required

# noinspection PyProtectedMember
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
