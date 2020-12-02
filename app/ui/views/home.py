from flask import render_template, redirect, url_for, current_app
from .. import blueprint
from app.model import Application


@blueprint.route("/")
def index():
    applications = Application.query.order_by(Application.name).all()

    return render_template("index.html", applications=applications)


@blueprint.route("/security_statement/<int:id>")
def security_statement(id):
    application = Application.query.get_or_404(id)

    return render_template("security_statement.html", application=application)


@blueprint.route("/security_statement/text/<int:id>")
def security_statement_text(id):
    application = Application.query.get_or_404(id)

    return '\n\n'.join([
        application.application_type.statement,
        application.hosting.statement,
        application.authentication.statement,
        application.visibility.statement,
    ])
