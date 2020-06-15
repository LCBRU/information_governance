from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    Boolean,
    UnicodeText,
)
from migrate.changeset.constraint import UniqueConstraint


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table(
        "statement",
        meta,
        Column("id", Integer, primary_key=True),
        Column("type", NVARCHAR(100), index=True, nullable=False),
        Column("name", NVARCHAR(100), index=True, nullable=False),
        Column("statement", UnicodeText, nullable=False),
        Column("last_updated_datetime", DateTime, nullable=False),
        Column("last_updated_by_user_id", Integer, nullable=False),
    )
    t.create()

    cons = UniqueConstraint(t.c.type, t.c.name, name='ux__statement__type__name')
    cons.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("statement", meta, autoload=True)
    t.drop()