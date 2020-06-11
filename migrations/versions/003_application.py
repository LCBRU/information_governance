from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    Boolean,
    ForeignKey,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    s = Table("statement", meta, autoload=True)
    u = Table("user", meta, autoload=True)

    t = Table(
        "application",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", NVARCHAR(100), unique=True, nullable=False),
        Column("application_type_id", Integer, ForeignKey(s.c.id), index=True, nullable=False),
        Column("hosting_id", Integer, ForeignKey(s.c.id), index=True, nullable=False),
        Column("visibility_id", Integer, ForeignKey(s.c.id), index=True, nullable=False),
        Column("authentication_id", Integer, ForeignKey(s.c.id), index=True, nullable=False),
        Column("last_updated_datetime", DateTime, nullable=False),
        Column("last_updated_by_user_id", Integer, ForeignKey(u.c.id), index=True, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("application", meta, autoload=True)
    t.drop()