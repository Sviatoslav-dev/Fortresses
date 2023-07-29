from sqlalchemy import create_engine

from db.models import users, units, meta


# engine = create_engine("postgresql+psycopg2://postgres:admin@localhost/fortresses", echo=True)
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
        self.engine = create_engine("postgresql+psycopg2://postgres:admin@localhost/fortresses",
                                    echo=True)
        meta.create_all(self.engine)

        self.conn = self.engine.connect()

    def __del__(self):
        self.conn.close()
        self.engine.dispose()

    def create_user(self, name, password, rating=0, stars=0):
        ins_users_query = users.insert().values(name=name, rating=rating,
                                                stars=stars, password=password)
        user_cursor = self.conn.execute(ins_users_query)
        self.conn.commit()
        return user_cursor.inserted_primary_key[0]

    def create_unit(self, user_id, unit_type, heath=0, heath_update_price=0,
                    damage=0, damage_update_price=0, step_price=0, steps=0, gold_price=0,
                    opened=False):
        ins_unit_query = units.insert().values(user_id=user_id, unit_type=unit_type, heath=heath,
                                               heath_update_price=heath_update_price,
                                               damage=damage,
                                               damage_update_price=damage_update_price,
                                               gold_price=gold_price, step_price=step_price,
                                               steps=steps, opened=opened)
        self.conn.execute(ins_unit_query)
        self.conn.commit()

    def get_users(self):
        users_gr_1000_query = users.select()
        result = self.conn.execute(users_gr_1000_query)
        self.conn.commit()

        res = []
        for row in result:
            res.append(dict(zip(row._fields, row._data)))
        return res

    def get_user(self, user_id):
        users_gr_1000_query = users.select().where(users.c.id == user_id)
        result = self.conn.execute(users_gr_1000_query)
        self.conn.commit()

        res = []
        for row in result:
            res.append(dict(zip(row._fields, row._data)))
        return res[0]

    def get_user_units(self, user_id):
        print("USER_ID: ", user_id)
        units_gr_1000_query = units.select().where(units.c.user_id == user_id)
        result = self.conn.execute(units_gr_1000_query)
        self.conn.commit()

        res = []
        for row in result:
            print(row)
            res.append(dict(zip(row._fields, row._data)))
        return res

    def get_user_unit(self, user_id, unit_type):
        units_gr_1000_query = units.select().where(
            units.c.user_id == user_id).where(units.c.unit_type == unit_type)
        request_result = self.conn.execute(units_gr_1000_query)
        self.conn.commit()

        res = []
        for row in request_result:
            res.append(dict(zip(row._fields, row._data)))
        return res[0]

    def create_user_with_default_units(self, name, password="qwe"):
        user_id = self.create_user(name, password)
        self.create_unit(user_id=user_id, unit_type="builder", heath=100, damage=0,
                         gold_price=20, step_price=5, steps=2, opened=True)
        self.create_unit(user_id=user_id, unit_type="swordsman", heath=120, heath_update_price=10,
                         damage=20, damage_update_price=10,
                         gold_price=25, step_price=5, steps=1, opened=True)
        self.create_unit(user_id=user_id, unit_type="archer", heath=80, heath_update_price=10,
                         damage=30, damage_update_price=10,
                         gold_price=30, step_price=5, steps=2, opened=True)
        return user_id

    def update_unit_skill(self, user_id, unit_type, skill):
        user = self.get_user(user_id)
        unit = self.get_user_unit(user_id, unit_type)

        if skill == "heath":
            if user["stars"] > unit["heath_update_price"]:
                query = units.update().where(units.c.user_id == user_id).where(
                                             units.c.unit_type == unit_type).values(
                    heath=unit["heath"] + 10)
                self.conn.execute(query)
                self.conn.commit()
                query = units.update().where(units.c.user_id == user_id).where(
                                             units.c.unit_type == unit_type).values(
                    heath_update_price=unit["heath_update_price"] + 2)
                self.conn.execute(query)
                self.conn.commit()

                self.add_user_stars(user_id, -unit["heath_update_price"])
        else:
            if user["stars"] > unit["damage_update_price"]:
                query = units.update().where(
                    units.c.user_id == user_id).where(units.c.unit_type == unit_type
                ).values(damage=unit["damage"] + 10)
                self.conn.execute(query)
                self.conn.commit()
                query = units.update().where(units.c.user_id == user_id).where(
                                             units.c.unit_type == unit_type).values(
                    damage_update_price=unit["damage_update_price"] + 2)
                self.conn.execute(query)
                self.conn.commit()

                self.add_user_stars(user_id, -unit["damage_update_price"])

    def open_unit(self, user_id, unit_type):
        user = self.get_user(user_id)
        if user["stars"] > 50:
            query = units.update().where(units.c.user_id == user_id).where(
                units.c.unit_type == unit_type).values(opened=True)
            self.conn.execute(query)
            self.conn.commit()

    def login(self, name, password):
        users_gr_1000_query = users.select(
        ).where(users.c.name == name).where(users.c.password == password)
        result = self.conn.execute(users_gr_1000_query)
        self.conn.commit()

        res = []
        for row in result:
            res.append(dict(zip(row._fields, row._data)))
        return res[0]["id"]


    def add_user_stars(self, user_id, stars):
        user = self.get_user(user_id)
        query = users.update().where(users.c.id == user_id).values(stars=user["stars"] + stars)
        self.conn.execute(query)
        self.conn.commit()

    def update_user_rating(self, user_id, plus_rating):
        user = self.get_user(user_id)
        query = users.update().where(users.c.id == user_id).values(
            rating=user["rating"] + plus_rating)
        self.conn.execute(query)
        self.conn.commit()


db = FortressDB()
# print(db.get_user_units(70))
# db.add_user_stars(1, 50)
# print(db.get_user(1))
# db.create_user_with_default_units("user1")
# db.create_user_with_default_units("user2")

# print(db.get_user(1))
# print(db.get_users())

db.update_unit_skill(70, "swordsman", "damage")
# print(db.get_user_units(1))
# print(db.get_user(1))
