import json

from db import db, text, exc


class DatabaseService:

    def form_query(self, sql, category=None, city=None, word=None):
        data = {}

        if category:
            data["category_id"] = tuple(category)
            sql += """ and res.id in (select restaurant_id from restaurants_categories
                where category_id in :category_id)"""
        if city:
            data["city"] = city.lower()
            sql += " and lower(location->>'city') = :city"
        if word:
            word = word.lower()
            data["word"] = word
            sql = (
                sql
                + """ and (lower(description) like '%' || :word || '%'
                or lower(name) like '%' || :word || '%')"""
            )
        return sql, data

    def get_all_columns_from_table(self, table, order_by=None, only_first_row=False):
        sql = "SELECT * FROM " + table
        if order_by:
            sql += " ORDER BY " + order_by
        result = db.session.execute(text(sql))
        if only_first_row:
            return result.fetchone()
        return result.fetchall()

    def add_user(self, username, password):
        sql = """INSERT INTO users (username, password, admin, created)
        VALUES (:username, :password, :admin, now())"""
        try:
            db.session.execute(
                text(sql), {"username": username, "password": password, "admin": False}
            )
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return "Tunnus on jo käytössä"
        return None

    def get_user(self, username):
        sql = "SELECT id, username, password, admin FROM users WHERE username=:username"
        result = db.session.execute(text(sql), {"username": username})
        return result.fetchone()

    def add_visit(self, usr_id):
        sql = "INSERT INTO visits (user_id, time) VALUES (:user_id, now())"
        db.session.execute(text(sql), {"user_id": usr_id})
        db.session.commit()

    def get_restaurant(self, restaurant_id, visible = True):
        sql = """SELECT id, name, description, location, opening_hours
                 FROM restaurants
                 WHERE visible = :visible and id = :id"""
        result = db.session.execute(text(sql), {"visible": visible, "id": restaurant_id})
        return result.fetchone()

    def get_restaurants(self, category="", city="", word=""):
        data = {}
        sql = """SELECT id, name, description, location, opening_hours
        FROM restaurants as res
        WHERE visible = true"""

        sql, data = self.form_query(sql, category,city,word)

        sql += " ORDER BY name"
        result = db.session.execute(
            text(sql),
            data,
        )
        return result.fetchall()

    def add_restaurant(self, name, description, location, opening_hours):
        sql = """INSERT INTO restaurants
        (name, description, location, opening_hours, visible, created)
        VALUES (:name,:description,:location,:opening_hours,:visible, now()) 
        RETURNING id"""

        if isinstance(location, dict):
            location = json.dumps(location, indent=4)

        result = db.session.execute(
            text(sql),
            {
                "name": name,
                "description": description,
                "location": location,
                "opening_hours": opening_hours,
                "visible": True,
            },
        )
        db.session.commit()
        return result.fetchone()[0]


    def update_restaurant(self, restaurant_id, name, description, location, opening_hours
    ):
        sql = """UPDATE restaurants SET
        name = :name, 
        description = :description, 
        location = :location, 
        opening_hours = :opening_hours, 
        visible = :visible,
        modified = now()
        WHERE id = :restaurant_id"""

        if isinstance(location, dict):
            location = json.dumps(location, indent=4)

        db.session.execute(
            text(sql),
            {
                "restaurant_id": restaurant_id,
                "name": name,
                "description": description,
                "location": location,
                "opening_hours": opening_hours,
                "visible": True,
            },
        )
        db.session.commit()

    def hide_restaurant(self, restaurant_id):
        sql = """UPDATE restaurants SET visible = :visible, modified = now()
                WHERE id = :restaurant_id"""
        try:
            db.session.execute(text(sql), {"restaurant_id": restaurant_id, "visible": False})
            db.session.commit()
        except Exception as error:
            print("Tapahtui virhe: ", error)
            db.session.rollback()
            return False
        return True

    def get_ratings(self, category=None, city=None, word=None):
        sql = """SELECT res.*,t.average, t.count
                 FROM restaurants res
                 INNER JOIN (
                    SELECT res.id, avg(ra.stars) as average, count(ra.stars) as count
                    FROM ratings as ra
                    LEFT JOIN restaurants as res ON res.id = ra.restaurant_id
                    WHERE res.visible is True and ra.visible is True"""

        sql, data = self.form_query(sql, category,city,word)

        sql += """ GROUP BY res.id ) as t on t.id=res.id
            ORDER BY t.average desc, t.count desc"""

        result = db.session.execute(text(sql), data)
        return result.fetchall()


    def get_rating_by_restaurant_and_user(self, user_id, restaurant_id):
        sql = """SELECT created FROM ratings
               WHERE user_id = :user_id AND restaurant_id = :restaurant_id
               ORDER BY created DESC"""
        result = db.session.execute(
            text(sql),
            {"restaurant_id": restaurant_id, "user_id": user_id},
        )

        if result.rowcount == 0:
            return None

        return result.fetchone()[0]

    def get_restaurants_ratings(self, restaurant_id, visible = True):
        sql = """SELECT r.id, stars, comment, r.created, u.username FROM ratings as r
        JOIN users as u on u.id = r.user_id
        WHERE restaurant_id = :restaurant_id and visible = :visible
        ORDER BY r.created desc"""

        result = db.session.execute(
            text(sql),
            {"restaurant_id": restaurant_id, "visible": visible},
        )
        return result.fetchall()

    def add_rating(self, user_id, restaurant_id, stars, comment):
        sql = """INSERT INTO ratings (user_id, restaurant_id, stars, comment, visible, created)
        VALUES (:user_id,:restaurant_id,:stars,:comment,:visible, now())"""
        db.session.execute(
            text(sql),
            {
                "user_id": user_id,
                "restaurant_id": restaurant_id,
                "stars": stars,
                "comment": comment,
                "visible": True,
            },
        )
        db.session.commit()

    def hide_rating(self, rating_id):
        sql = (
            "UPDATE ratings SET visible = :visible, modified = now() WHERE id = :rating_id"
        )
        db.session.execute(text(sql), {"rating_id": rating_id, "visible": False})
        db.session.commit()

    def add_category(self, name):
        sql = "INSERT INTO categories (name, created) VALUES (:name, now())"
        try:
            db.session.execute(text(sql), {"name": name})
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return "Kategoria on jo olemassa"
        return None


    def delete_category(self, category_id):
        sql = "DELETE FROM categories WHERE id = :category_id"
        db.session.execute(text(sql), {"category_id": category_id})
        db.session.commit()


    def get_restaurant_categories(self, restaurant_id):
        sql = """SELECT cat.id, cat.name
                 FROM restaurants_categories as res_cat
                 JOIN categories cat ON cat.id = res_cat.category_id 
                 WHERE restaurant_id = :restaurant_id"""
        result = db.session.execute(text(sql), {"restaurant_id": restaurant_id})
        return result.fetchall()

    def add_restaurant_category(self, restaurant_id, categories_id):
        data = {}
        data["restaurant_id"] = restaurant_id
        sql = "DELETE FROM restaurants_categories WHERE restaurant_id = :restaurant_id"
        if categories_id:
            sql += " AND category_id NOT IN :categories"
            data["categories"] = tuple(categories_id)
        db.session.execute(text(sql), data)
        for category_id in categories_id:
            sql = """INSERT INTO restaurants_categories (restaurant_id, category_id)
                     SELECT :restaurant_id, :category_id
                     ON CONFLICT (restaurant_id, category_id) DO NOTHING"""
            db.session.execute(
                text(sql), {"restaurant_id": restaurant_id, "category_id": category_id}
            )
        db.session.commit()

    def get_categories_and_restaurants(self):
        sql = """SELECT cat.id, cat.name, res.name as restaurant,
        res.location->>'city' as city, count(res_cat.restaurant_id) as count
        FROM categories as cat
        LEFT JOIN restaurants_categories as res_cat ON res_cat.category_id = cat.id
        LEFT JOIN restaurants as res ON res.id = res_cat.restaurant_id
        GROUP BY cat.id, cat.name, res.name, res.location->>'city'
        ORDER BY cat.name"""
        result = db.session.execute(text(sql))
        return result.fetchall()

    def delete_image(self, restaurant_id):
        sql = "DELETE FROM images WHERE restaurant_id = :restaurant_id"
        db.session.execute(text(sql), {"restaurant_id": restaurant_id})
        db.session.commit()

    def upload_image(self, restaurant_id, name, data):
        sql = "INSERT INTO images (restaurant_id, name, data) VALUES (:restaurant_id, :name, :data)"
        db.session.execute(text(sql), {"restaurant_id":restaurant_id, "name":name, "data":data})
        db.session.commit()

    def download_image(self, restaurant_id):
        sql = "SELECT data FROM images WHERE restaurant_id = :restaurant_id"
        result = db.session.execute(text(sql), {"restaurant_id":restaurant_id})
        if result.rowcount == 0:
            return None
        return result.fetchone()[0]


database_service = DatabaseService()
