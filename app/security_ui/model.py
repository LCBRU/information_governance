import ldap
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from app.database import db
from app.utils import log_exception


def search_ldap(user):
    proxy = {
        'username': user.username,
        'email': '',
        'name': '',
        'surname': user.last_name,
        'given_name': user.first_name,
    }

    if current_app.config['FLASK_DEBUG']:
        return proxy

    l = ldap.initialize(current_app.config['LDAP_URI'])
    l.protocol_version = 3
    l.set_option(ldap.OPT_REFERRALS, 0)

    try:
        l.simple_bind_s(
            current_app.config['LDAP_USER'],
            current_app.config['LDAP_PASSWORD'],
        )

        search_result = l.search_s(
            'DC=xuhl-tr,DC=nhs,DC=uk',
            ldap.SCOPE_SUBTREE,
            'sAMAccountName={}'.format(user.username),
        )

    except ldap.LDAPError as e:
        log_exception(e)

    if isinstance(search_result[0][1], dict):
        ldap_user = search_result[0][1]
        return {
            'username': ldap_user['sAMAccountName'][0].decode("utf-8"),
            'email': ldap_user['mail'][0].decode("utf-8"),
            'name': ldap_user['name'][0].decode("utf-8"),
            'surname': ldap_user['sn'][0].decode("utf-8"),
            'given_name': ldap_user['givenName'][0].decode("utf-8"),
        }
    else:
        return proxy


def validate_password(user, password):
    if current_app.config['FLASK_DEBUG']:
        current_app.logger.info('In debug skipping LDAP lookup')
        return True

    current_app.logger.info('Contacting LDAP Server: %s', current_app.config['LDAP_URI'])
    
    l = ldap.initialize(current_app.config['LDAP_URI'])
    l.protocol_version = 3
    l.set_option(ldap.OPT_REFERRALS, 0)

    try:
        current_app.logger.info('LDAP Binding')
        l.simple_bind_s(user.email, password)
        return True

    except ldap.LDAPError as e:
        current_app.logger.info('LDAP Error')
        return False


def validate_password_uhl(user, password):
    if current_app.config['FLASK_DEBUG']:
        current_app.logger.info('In debug skipping LDAP lookup')
        return True

    current_app.logger.info('Contacting LDAP Server: %s', current_app.config['LDAP_URI'])
    
    l = ldap.initialize(current_app.config['LDAP_URI'])
    l.protocol_version = 3
    l.set_option(ldap.OPT_REFERRALS, 0)

    try:
        current_app.logger.info('LDAP Binding')
        l.simple_bind_s(user.email, password)
        return True

    except ldap.LDAPError as e:
        current_app.logger.info('LDAP Error')
        return False


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active

    @property
    def full_name(self):
        return self.username
        # user = search_ldap(self)
        # return "{} {}".format(user['given_name'], user['surname']).strip()

    @property
    def email(self):
        return self.username
        # user = search_ldap(self)
        # return user['email']

    def __str__(self):
        return self.email or self.username
