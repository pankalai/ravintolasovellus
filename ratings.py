from db import db, text


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
            + """ and res.id in (select restaurant_id from restaurants_categories
            where category_id in :category_id)"""
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
