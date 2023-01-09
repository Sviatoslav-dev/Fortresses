from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, Boolean

meta = MetaData()

users = Table(
    'Users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(250), nullable=False, unique=True),
    Column('rating', Integer, default=0),
    Column('stars', Integer, default=0),
)

units = Table(
    'Units', meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("Users.id")),
    Column('unit_type', String(250), nullable=False),
    Column('heath', Integer, default=0),
    Column('heath_update_price', Integer, default=0),
    Column('damage', Integer, default=0),
    Column('damage_update_price', Integer, default=0),
    Column('gold_price', Integer, default=0),
    Column("step_price", Integer, default=0),
    Column("steps", Integer, default=0),
    Column('opened', Boolean, nullable=False, default=False),
)
