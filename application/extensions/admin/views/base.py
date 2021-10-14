from flask_admin.contrib import sqla

from application.extensions.auth import login_required


class BaseView(sqla.ModelView):
    @login_required
    def _handle_view(self, name, **kwargs):
        pass
