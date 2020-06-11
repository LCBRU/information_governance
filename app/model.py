from datetime import datetime
from .database import db
from .security_ui.model import User


class Statement(db.Model):
    __tablename__ = 'statement'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), index=True)
    name = db.Column(db.String(100), unique=True)
    statement = db.Column(db.UnicodeText)
    last_updated_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated_by_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    last_updated_by_user = db.relationship(User)

    __mapper_args__ = {
        'polymorphic_identity':'Statement',
        'polymorphic_on':type
    }

    def __str__(self):
        return self.name



class HostingStatement(Statement):
    __mapper_args__ = {
        'polymorphic_identity':'Hosting',
    }


class AuthenticationStatement(Statement):
    __mapper_args__ = {
        'polymorphic_identity':'Authentication',
    }


class ApplicationTypeStatement(Statement):
    __mapper_args__ = {
        'polymorphic_identity':'ApplicationType',
    }


class VisibilityStatement(Statement):
    __mapper_args__ = {
        'polymorphic_identity':'Visibility',
    }


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    application_type_id = db.Column(db.Integer, db.ForeignKey(ApplicationTypeStatement.id))
    application_type = db.relationship(ApplicationTypeStatement, foreign_keys=[application_type_id])
    hosting_id = db.Column(db.Integer, db.ForeignKey(HostingStatement.id))
    hosting = db.relationship(HostingStatement, foreign_keys=[hosting_id])
    visibility_id = db.Column(db.Integer, db.ForeignKey(VisibilityStatement.id))
    visibility = db.relationship(VisibilityStatement, foreign_keys=[visibility_id])
    authentication_id = db.Column(db.Integer, db.ForeignKey(AuthenticationStatement.id))
    authentication = db.relationship(AuthenticationStatement, foreign_keys=[authentication_id])
    last_updated_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated_by_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    last_updated_by_user = db.relationship(User)
