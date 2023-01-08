from sqlalchemy import create_engine

from db.models import users, units, meta

engine = create_engine("postgresql+psycopg2://sviatoslav:8745@localhost/fortresses", echo=True)
meta.create_all(engine)
conn = engine.connect()

# query = f'DROP TABLE "Units";'
# conn.execute(query)
#
# query = f'DROP TABLE "Users";'
# conn.execute(query)


class FortressDB:
    def __init__(self):
        engine = create_engine("postgresql+psycopg2://sviatoslav:8745@localhost/fortresses", echo=True)
        meta.create_all(engine)

        self.conn = engine.connect()

    def create_user(self, name):
        ins_users_query = users.insert().values(name=name)
        self.conn.execute(ins_users_query)

    def create_unit(self, user_id, unit_type, heath, damage, price, opened):
        ins_unit_query = units.insert().values(user_id=user_id, unit_type=unit_type, heath=heath, damage=damage,
                                               price=price, opened=opened)
        self.conn.execute(ins_unit_query)

    def get_users(self):
        users_gr_1000_query = users.select()
        result = self.conn.execute(users_gr_1000_query)

        res = []
        for row in result:
            res.append(dict(row))
        return res

    def get_user_units(self, user_id):
        print("USER_ID: ", user_id)
        units_gr_1000_query = units.select().where(units.c.user_id == user_id)
        result = self.conn.execute(units_gr_1000_query)

        res = []
        for row in result:
            res.append(dict(row))
        return res


db = FortressDB()
# db.create_user("user1")
# db.create_unit(1, "builder", 100, 0, 40, True)
# db.get_user_units(1)
