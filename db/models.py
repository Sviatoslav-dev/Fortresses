from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, Boolean

# Метаданные-это информация о данных в БД; например, информация о таблицах и столбцах, в которых мы храним данные.
meta = MetaData()

# создаём таблицы
users = Table(
    'Users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(250), nullable=False, unique=True)
)

units = Table(
    'Units', meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("Users.id")),
    Column('unit_type', String(250), nullable=True),
    Column('heath', Integer, nullable=True),
    Column('damage', Integer, nullable=True),
    Column('price', Integer, nullable=True),
    Column('opened', Boolean, nullable=True),
)
