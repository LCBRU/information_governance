import time
from functools import wraps
from flask import g, current_app
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
)
from .model import User, validate_password
from .database import db


SYSTEM_USER_NAME = 'system'

login_manager = LoginManager()


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).one_or_none()


def init_security(app):
    login_manager.init_app(app)
    login_manager.login_view = "security_ui.login"

    @app.before_first_request
    def init_data():
        _init_users()

def _init_users():
    if User.query.filter_by(username=current_app.config['ADMIN_USER_USERNAME']).count() == 0:
        admin = User(
            username=current_app.config['ADMIN_USER_USERNAME'],
            first_name=current_app.config['ADMIN_USER_FIRST_NAME'],
            last_name=current_app.config['ADMIN_USER_LAST_NAME'],
        )
        db.session.add(admin)

    db.session.commit()


def login(username, password):
    current_app.logger.info('Username supplied for login: %s', username)

    user = User.query.filter_by(username=username).first()

    current_app.logger.info('User attempting log in: %s', user)

    if user:
        if user.is_active:
            if validate_password(user, password):
                login_user(user)
                current_app.logger.info('User logged in: %s', user.username)
                return user
    
    time.sleep(2)
