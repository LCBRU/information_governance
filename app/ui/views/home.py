from flask import render_template, redirect, url_for, current_app
from .. import blueprint
from app.model import Application


@blueprint.route("/")
def index():
    applications = Application.query.order_by(Application.name).all()

    current_app.logger.info('Application_root: %s', current_app.wsgi_app.script_name)

    return render_template("index.html", applications=applications)


@blueprint.route("/security_statement/<int:id>")
def security_statement(id):
    application = Application.query.get_or_404(id)

    return render_template("security_statement.html", application=application)
