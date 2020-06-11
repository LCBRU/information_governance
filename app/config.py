import os
from dotenv import load_dotenv

# Load environment variables from '.env' file.
load_dotenv()


class BaseConfig(object):
    SITE_NAME = 'Information Governance'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False") == 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_DATABASE_URI = os.environ["DB_URI"]

    ADMIN_USER_USERNAME = os.environ["ADMIN_USER_USERNAME"]
    ADMIN_USER_FIRST_NAME = os.environ["ADMIN_USER_FIRST_NAME"]
    ADMIN_USER_LAST_NAME = os.environ["ADMIN_USER_LAST_NAME"]


class TestConfig(BaseConfig):
    """Configuration for general testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False


class TestConfigCRSF(TestConfig):
    WTF_CSRF_ENABLED = True
