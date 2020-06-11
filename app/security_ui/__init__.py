#!/usr/bin/env python3

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
from flask_login import logout_user
from .forms import LoginForm
from ..database import db
from ..model import User
from ..security import login as login_user


blueprint = Blueprint("security_ui", __name__, template_folder="templates")

@blueprint.record
def record(state):
    if db is None:
        raise Exception(
            "This blueprint expects you to provide database access through database"
        )


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
        user = login_user(form.username.data, form.password.data)

        current_app.logger.info('Logged in user: %s', user)

        return redirect(next_url or url_for('ui.labels'))

    return render_template('login.html', form=form, next_url=next_url)


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('ui.labels'))
