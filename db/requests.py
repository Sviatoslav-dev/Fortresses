from sqlalchemy import create_engine

from db.models import users, units, meta


# engine = create_engine("postgresql+psycopg2://sviatoslav:8745@localhost/fortresses", echo=True)
# meta.create_all(engine)
# conn = engine.connect()
#
# ins_users_query = users.insert().values(name="ssdf4")
# conn_res = conn.execute(ins_users_query)
# print(conn_res.inserted_primary_key[0])

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

    def create_user(self, name, rating=0, stars=0):
        ins_users_query = users.insert().values(name=name, rating=rating, stars=stars)
        user_cursor = self.conn.execute(ins_users_query)
        return user_cursor.inserted_primary_key[0]

    def create_unit(self, user_id, unit_type, heath=0, heath_update_price=0,
                    damage=0, damage_update_price=0, step_price=0, steps=0, gold_price=0, opened=False):
        ins_unit_query = units.insert().values(user_id=user_id, unit_type=unit_type, heath=heath,
                                               heath_update_price=heath_update_price,
                                               damage=damage, damage_update_price=damage_update_price,
                                               gold_price=gold_price, step_price=step_price, steps=steps, opened=opened)
        self.conn.execute(ins_unit_query)

    def get_users(self):
        users_gr_1000_query = users.select()
        result = self.conn.execute(users_gr_1000_query)

        res = []
        for row in result:
            res.append(dict(row))
        return res

    def get_user(self, user_id):
        users_gr_1000_query = users.select().where(users.c.id == user_id)
        result = self.conn.execute(users_gr_1000_query)

        res = []
        for row in result:
            res.append(dict(row))
        return res[0]

    def get_user_units(self, user_id):
        print("USER_ID: ", user_id)
        units_gr_1000_query = units.select().where(units.c.user_id == user_id)
        result = self.conn.execute(units_gr_1000_query)

        res = []
        for row in result:
            res.append(dict(row))
        return res

    def get_user_unit(self, user_id, unit_type):
        units_gr_1000_query = units.select().where(units.c.user_id == user_id and units.c.unit_type == unit_type)
        request_result = self.conn.execute(units_gr_1000_query)

        res = []
        for row in request_result:
            res.append(dict(row))
        return res[0]

    def create_user_with_default_units(self, name):
        user_id = self.create_user(name)
        self.create_unit(user_id=user_id, unit_type="builder", heath=100, damage=0,
                         gold_price=20, step_price=5, steps=2, opened=True)
        self.create_unit(user_id=user_id, unit_type="swordsman", heath=120, heath_update_price=10,
                         damage=20, damage_update_price=10,
                         gold_price=25, step_price=5, steps=1, opened=True)
        self.create_unit(user_id=user_id, unit_type="archer", heath=80, heath_update_price=10,
                         damage=30, damage_update_price=10,
                         gold_price=30, step_price=5, steps=2, opened=True)

    def update_unit_skill(self, user_id, unit_type, skill):
        user = self.get_user(user_id)
        unit = self.get_user_unit(user_id, unit_type)

        if skill == "heath":
            if user["stars"] > unit["heath_update_price"]:
                query = units.update().where(units.c.user_id == user_id and
                                             units.c.unit_type == unit_type).values(heath=unit["heath"] + 10)
                self.conn.execute(query)
                query = units.update().where(units.c.user_id == user_id and
                                             units.c.unit_type == unit_type).values(
                    heath_update_price=unit["heath_update_price"] + 2)
                self.conn.execute(query)

                self.add_user_stars(user_id, -unit["heath_update_price"])
        else:
            if user["stars"] > unit["damage_update_price"]:
                query = units.update().where(units.c.user_id == user_id and
                                             units.c.unit_type == unit_type).values(damage=unit["damage"] + 10)
                self.conn.execute(query)
                query = units.update().where(units.c.user_id == user_id and
                                             units.c.unit_type == unit_type).values(
                    damage_update_price=unit["damage_update_price"] + 2)
                self.conn.execute(query)

                self.add_user_stars(user_id, -unit["damage_update_price"])

    def add_user_stars(self, user_id, stars):
        user = self.get_user(user_id)
        query = users.update().where(users.c.id == user_id).values(stars=user["stars"] + stars)
        self.conn.execute(query)


db = FortressDB()
# db.add_user_stars(1, 50)
# print(db.get_user(1))
# db.create_user_with_default_units("user1")
# db.create_user_with_default_units("user2")

# db.update_unit_skill(1, "swordsman", "heath")
# print(db.get_user_units(1))
# print(db.get_user(1))
