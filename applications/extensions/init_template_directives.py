from flask import session, current_app
from flask_login import current_user
from flask_wtf.csrf import generate_csrf


def init_template_directives(app):
    @app.template_global()
    def authorize(power):
        if current_user.username != current_app.config.get("SUPERADMIN"):
            return bool(power in session.get('permissions'))
        else:
            return True

    @app.template_global()
    def csrf_input():
        return f'<input type="hidden" name="csrf_token" value="{generate_csrf()}">'

