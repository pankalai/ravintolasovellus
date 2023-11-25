import json
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


# Restaurants


def add_restaurant(name, description, location, opening_hours):
    sql = """INSERT INTO restaurants (name, description, location, opening_hours, visible, created)
    VALUES (:name,:description,:location,:opening_hours,:visible, now())"""

    if type(location) is dict:
        location = json.dumps(location, indent=4)

    db.session.execute(
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


def get_restaurants(category="", city="", description=""):
    data = {}
    sql = "SELECT * FROM restaurants WHERE visible = true"

    if category:
        pass
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


def get_restaurant(restaurant_id):
    sql = "SELECT * FROM restaurants WHERE id = :id"
    result = db.session.execute(text(sql), {"id": restaurant_id})
    return result.fetchone()


def update_restaurant(restaurant_id, name, description, location, opening_hours):
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
    sql = """SELECT r.*,t.average, t.count
    FROM restaurants r
    INNER JOIN (
    SELECT re.id, avg(ra.stars) as average, count(ra.stars) as count
    FROM ratings as ra
    LEFT JOIN restaurants as re ON re.id = ra.restaurant_id
    WHERE re.visible is True and ra.visible is True"""
    data = {}
    if category:
        pass
    if city:
        data["city"] = city.lower()
        sql = sql + " and lower(location->>'city') = :city"

    sql = sql + " GROUP BY re.id ) as t on t.id=r.id"

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
