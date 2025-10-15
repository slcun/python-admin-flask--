from flask import Flask

from .admin import admin_cli
from .check import check_cli
from applications.extensions.init_plugins import broadcast_execute


def init_script(app: Flask):
    app.cli.add_command(admin_cli)
    app.cli.add_command(check_cli)
    broadcast_execute(app, 'event_finish')
