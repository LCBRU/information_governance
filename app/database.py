from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from contextlib import contextmanager
from flask import current_app


db = SQLAlchemy()
