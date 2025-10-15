from flask import Flask
from .init_sqlalchemy import db, ma, init_databases
from .init_login import init_login_manager
from .init_template_directives import init_template_directives
from .init_error_views import init_error_views
from .init_mail import init_mail, mail as flask_mail
from .init_upload import init_upload
from .init_migrate import init_migrate
from .init_session import init_session
from .init_limit import init_limit
from .init_plugins import register_plugin, broadcast_execute


def init_plugs(app: Flask) -> None:
    # 注册插件
    register_plugin(app)
    broadcast_execute(app, 'event_begin')

    # 注册 Flask 功能
    init_login_manager(app)
    init_databases(app)
    init_mail(app)
    init_upload(app)
    init_migrate(app)
    init_session(app)
    init_limit(app)

    # 系统蓝图相关
    init_template_directives(app)
    init_error_views(app)
