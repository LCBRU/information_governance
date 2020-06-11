from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    Boolean,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table(
        "user",
        meta,
        Column("id", Integer, primary_key=True),
        Column("username", NVARCHAR(100), index=True, nullable=False, unique=True),
        Column("first_name", NVARCHAR(50), nullable=False),
        Column("last_name", NVARCHAR(50), nullable=False),
        Column("active", Boolean(), nullable=False),
        Column("created_datetime", DateTime, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("user", meta, autoload=True)
    t.drop()