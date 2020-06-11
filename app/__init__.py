import os
import logging
from flask import Flask
from .ui import blueprint as ui_blueprint
from .security_ui import blueprint as security_blueprint
from .database import db
from .template_filters import init_template_filters
from .standard_views import init_standard_views
from .utils import ReverseProxied
from .config import BaseConfig
from .admin import init_admin


def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.config.from_object(config)
    app.config.from_pyfile("application.cfg", silent=True)

    with app.app_context():
        app.logger.setLevel(logging.INFO)
        db.init_app(app)
        init_template_filters(app)
        init_standard_views(app)
        init_admin(app)

    app.register_blueprint(ui_blueprint)
    app.register_blueprint(security_blueprint)

    return app
