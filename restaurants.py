import json
from db import db, text
import categories


def add_restaurant(name, description, location, opening_hours, cat):
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

    categories.add_restaurant_category(restaurant_id, cat)


def get_restaurants(category="", city="", word=""):
    data = {}
    sql = """SELECT id, name, description, location, opening_hours
    FROM restaurants as res
    WHERE visible = true"""

    if category:
        data["category_id"] = tuple(category)
        sql = (
            sql
            + """ and res.id in (select restaurant_id from restaurants_categories
            where category_id in :category_id)"""
        )
    if city:
        data["city"] = city.lower()
        sql = sql + " and lower(location->>'city') = :city"
    if word:
        data["word"] = word.lower()
        # This needs to be modified
        sql = (
            sql
            + f""" and (lower(description) like '%{word.lower()}%'
            or lower(name) like '%{word.lower()}%')"""
        )

    sql += " ORDER BY name"
    result = db.session.execute(
        text(sql),
        data,
    )
    return result.fetchall()


def get_restaurant(restaurant_id, visible: bool = True):
    sql = """SELECT id, name, description, location, opening_hours FROM restaurants
    WHERE visible = :visible and id = :id"""
    result = db.session.execute(text(sql), {"visible": visible, "id": restaurant_id})
    return result.fetchone()


def update_restaurant(
    restaurant_id, name, description, location, opening_hours, cat=None
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

    if cat:
        categories.add_restaurant_category(restaurant_id, cat)


def hide_restaurant(restaurant_id):
    sql = "UPDATE restaurants SET visible = :visible, modified = now() WHERE id = :restaurant_id"
    db.session.execute(text(sql), {"restaurant_id": restaurant_id, "visible": False})
    db.session.commit()
