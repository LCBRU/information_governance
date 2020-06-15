from sqlalchemy import (
    MetaData,
    Table,
    Column,
    UnicodeText,
)


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t = Table("application", meta, autoload=True)

    column = Column("description", UnicodeText)
    column.create(t)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table("application", meta, autoload=True)
    t.c.description.drop()
