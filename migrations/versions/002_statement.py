from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    Boolean,
    String,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table(
        "statement",
        meta,
        Column("id", Integer, primary_key=True),
        Column("type", NVARCHAR(100), unique=True, nullable=False),
        Column("name", NVARCHAR(100), unique=True, nullable=False),
        Column("statement", NVARCHAR, nullable=False),
        Column("last_updated_datetime", DateTime, nullable=False),
        Column("last_updated_by_user_id", Integer, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("statement", meta, autoload=True)
    t.drop()