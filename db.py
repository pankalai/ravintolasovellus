import json
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


# Restaurants


def add_restaurant(name, description, location, opening_hours, categories):
    sql = """INSERT INTO restaurants (name, description, location, opening_hours, visible, created)
    VALUES (:name,:description,:location,:opening_hours,:visible, now()) RETURNING id"""

    if type(location) is dict:
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
    restaurant_id = result.fetchone()[0]
    db.session.commit()

    add_restaurant_category(restaurant_id, categories)


def get_restaurants(category="", city="", description=""):
    data = {}
    sql = """SELECT id, name, description, location, opening_hours 
    FROM restaurants as res
    WHERE visible = true"""

    if category:
        data["category_id"] = tuple(category)
        sql = (
            sql
            + " and res.id in (select restaurant_id from restaurants_categories where category_id in :category_id)"
        )
    if city:
        data["city"] = city.lower()
        sql = sql + " and lower(location->>'city') = :city"
    if description:
        data["description"] = description.lower()
        # This needs to be modified
        sql = (
            sql
            + f""" and (lower(description) like '%{description.lower()}%'
            or lower(name) like '%{description.lower()}%')"""
        )

    result = db.session.execute(
        text(sql),
        data,
    )
    return result.fetchall()


def get_restaurant(restaurant_id, visible: bool = True):
    sql = "SELECT id, name, description, location, opening_hours FROM restaurants WHERE visible = :visible and id = :id"
    result = db.session.execute(text(sql), {"visible": visible, "id": restaurant_id})
    return result.fetchone()


def update_restaurant(
    restaurant_id, name, description, location, opening_hours, categories=None
):
    sql = """UPDATE restaurants SET
    name = :name, 
    description = :description, 
    location = :location, 
    opening_hours = :opening_hours, 
    visible = :visible,
    modified = now()
    WHERE id = :restaurant_id"""

    if type(location) is dict:
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

    if categories:
        add_restaurant_category(restaurant_id, categories)


def hide_restaurant(restaurant_id):
    sql = "UPDATE restaurants SET visible = :visible, modified = now() WHERE id = :restaurant_id"
    db.session.execute(text(sql), {"restaurant_id": restaurant_id, "visible": False})
    db.session.commit()


# Ratings


def add_rating(user_id, restaurant_id, stars, comment):
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


def get_ratings(category=None, city=None):
    sql = """SELECT res.*,t.average, t.count
    FROM restaurants res
    INNER JOIN (
    SELECT res.id, avg(ra.stars) as average, count(ra.stars) as count
    FROM ratings as ra
    LEFT JOIN restaurants as res ON res.id = ra.restaurant_id
    WHERE res.visible is True and ra.visible is True"""
    data = {}
    if category:
        data["category_id"] = tuple(category)
        sql = (
            sql
            + " and res.id in (select restaurant_id from restaurants_categories where category_id in :category_id)"
        )
    if city:
        data["city"] = city.lower()
        sql = sql + " and lower(location->>'city') = :city"

    sql = sql + " GROUP BY res.id ) as t on t.id=res.id"

    result = db.session.execute(text(sql), data)
    return result.fetchall()


def get_restaurants_ratings(restaurant_id):
    sql = """SELECT r.id, stars, comment, r.created, u.username FROM ratings as r
    JOIN users as u on u.id = r.user_id
    WHERE restaurant_id = :restaurant_id and visible = :visible"""

    result = db.session.execute(
        text(sql),
        {"restaurant_id": restaurant_id, "visible": True},
    )
    return result.fetchall()


def hide_rating(rating_id):
    sql = (
        "UPDATE ratings SET visible = :visible, modified = now() WHERE id = :rating_id"
    )
    db.session.execute(text(sql), {"rating_id": rating_id, "visible": False})
    db.session.commit()


# Users


def login(username):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username": username})
    return result.fetchone()


def register(username, hash_value):
    sql = """INSERT INTO users (username, password, admin, created)
    VALUES (:username, :password, :admin, now())"""
    db.session.execute(
        text(sql), {"username": username, "password": hash_value, "admin": False}
    )
    db.session.commit()


def add_visit(user_id):
    sql = "INSERT INTO visits (user_id, time) VALUES (:user_id, now())"
    db.session.execute(text(sql), {"user_id": user_id})
    db.session.commit()


# Categories


def get_categories(id=None):
    sql = "SELECT id, name FROM categories"
    result = db.session.execute(text(sql))
    return result.fetchall()


def get_categories_and_restaurants():
    sql = """SELECT cat.id, cat.name, res.name as restaurant, res.location->>'city' as city, count(res_cat.restaurant_id) as count
    FROM categories as cat
    LEFT JOIN restaurants_categories as res_cat ON res_cat.category_id = cat.id
    LEFT JOIN restaurants as res ON res.id = res_cat.restaurant_id
    GROUP BY cat.id, cat.name, res.name, res.location->>'city'"""
    result = db.session.execute(text(sql))
    return result.fetchall()


def add_category(name):
    sql = "INSERT INTO categories (name, created) VALUES (:name, now())"
    db.session.execute(text(sql), {"name": name})
    db.session.commit()


def get_restaurant_category(restaurant_id):
    sql = """SELECT cat.id, cat.name FROM restaurants_categories as res_cat 
    JOIN categories cat ON cat.id = res_cat.category_id 
    WHERE restaurant_id = :restaurant_id"""
    result = db.session.execute(text(sql), {"restaurant_id": restaurant_id})
    return result.fetchall()


def add_restaurant_category(restaurant_id, categories_id):
    sql = "DELETE FROM restaurants_categories WHERE restaurant_id = :restaurant_id"
    db.session.execute(text(sql), {"restaurant_id": restaurant_id})
    for category_id in categories_id:
        sql = "INSERT INTO restaurants_categories (restaurant_id, category_id) VALUES (:restaurant_id, :category_id)"
        db.session.execute(
            text(sql), {"restaurant_id": restaurant_id, "category_id": category_id}
        )
    db.session.commit()
