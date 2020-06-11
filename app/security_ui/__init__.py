import time
import logging
from urllib.parse import urlparse, urljoin
from flask import (
    Blueprint,
    render_template,
    redirect,
    abort,
    url_for,
    flash,
    request,
    current_app,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
)
from .forms import LoginForm
from ..database import db
from .model import User, validate_password


blueprint = Blueprint("security_ui", __name__, template_folder="templates")
login_manager = LoginManager()


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).one_or_none()


@blueprint.record
def record(state):
    if db is None:
        raise Exception(
            "This blueprint expects you to provide database access through database"
        )
    
    login_manager.init_app(state.app)
    login_manager.login_view = "security_ui.login"

    @state.app.before_first_request
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


def _login(username, password):
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


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@blueprint.route("/login",methods=["GET", "POST"])
def login():
    next_url = request.args.get('next')
    if not is_safe_url(next_url):
        return abort(400)

    form = LoginForm()

    if form.validate_on_submit():
        user = _login(form.username.data, form.password.data)

        current_app.logger.info('Logged in user: %s', user)

        return redirect(next_url or url_for('ui.index'))

    return render_template('login.html', form=form, next_url=next_url)


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('ui.index'))
