import datetime
import flask_admin as admin
from flask import current_app, redirect, url_for, request
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView, fields
from flask_login import current_user
from .database import db
from .model import (
    HostingStatement,
    Application,
    ApplicationTypeStatement,
    VisibilityStatement,
    AuthenticationStatement,
)


class QuerySelectMultipleFieldSet(fields.QuerySelectMultipleField):
    def populate_obj(self, obj, name):
        setattr(obj, name, set(self.data))


class CustomView(ModelView):
    # Enable CSRF
    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security_ui.login', next=request.url))

    def on_model_change(self, form, model, is_created):
        model.last_updated_datetime = datetime.datetime.utcnow()
        model.last_updated_by_user = current_user


class StatementView(CustomView):
    column_list = form_columns = ["name", "statement"]


class ApplicationView(CustomView):
    column_list = form_columns = ["name", "application_type", "hosting", "visibility", "authentication"]

    form_args = {
        'application_type': {
            'query_factory': lambda: db.session.query(ApplicationTypeStatement)
        },
        'hosting': {
            'query_factory': lambda: db.session.query(HostingStatement)
        },
        'visibility': {
            'query_factory': lambda: db.session.query(VisibilityStatement)
        },
        'authentication': {
            'query_factory': lambda: db.session.query(AuthenticationStatement)
        },
    }


def init_admin(app):
    flask_admin = admin.Admin(app, name=current_app.config['SITE_NAME'], url="/admin")
    flask_admin.add_view(StatementView(HostingStatement, db.session))
    flask_admin.add_view(StatementView(ApplicationTypeStatement, db.session))
    flask_admin.add_view(StatementView(VisibilityStatement, db.session))
    flask_admin.add_view(StatementView(AuthenticationStatement, db.session))
    flask_admin.add_view(ApplicationView(Application, db.session))
