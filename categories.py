from db import db, text


def get_categories():
    sql = "SELECT id, name FROM categories ORDER BY name"
    result = db.session.execute(text(sql))
    return result.fetchall()


def get_categories_and_restaurants():
    sql = """SELECT cat.id, cat.name, res.name as restaurant,
    res.location->>'city' as city, count(res_cat.restaurant_id) as count
    FROM categories as cat
    LEFT JOIN restaurants_categories as res_cat ON res_cat.category_id = cat.id
    LEFT JOIN restaurants as res ON res.id = res_cat.restaurant_id
    GROUP BY cat.id, cat.name, res.name, res.location->>'city'
    ORDER BY cat.name"""
    result = db.session.execute(text(sql))
    return result.fetchall()


def get_restaurant_category(restaurant_id):
    sql = """SELECT cat.id, cat.name FROM restaurants_categories as res_cat
    JOIN categories cat ON cat.id = res_cat.category_id 
    WHERE restaurant_id = :restaurant_id"""
    result = db.session.execute(text(sql), {"restaurant_id": restaurant_id})
    return result.fetchall()


def add_category(name):
    sql = "INSERT INTO categories (name, created) VALUES (:name, now())"
    db.session.execute(text(sql), {"name": name})
    db.session.commit()


def add_restaurant_category(restaurant_id, categories_id):
    sql = "DELETE FROM restaurants_categories WHERE restaurant_id = :restaurant_id"
    db.session.execute(text(sql), {"restaurant_id": restaurant_id})
    for category_id in categories_id:
        sql = """INSERT INTO restaurants_categories (restaurant_id, category_id)
        VALUES (:restaurant_id, :category_id)"""
        db.session.execute(
            text(sql), {"restaurant_id": restaurant_id, "category_id": category_id}
        )
    db.session.commit()


def delete_category(category_id):
    sql = "DELETE FROM categories WHERE id = :category_id"
    db.session.execute(text(sql), {"category_id": category_id})
    db.session.commit()
