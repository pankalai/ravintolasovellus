from secrets import token_hex
import re
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db, text


def get_user(username):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username": username})
    return result.fetchone()


def exec_register(username, hash_value):
    sql = """INSERT INTO users (username, password, admin, created)
    VALUES (:username, :password, :admin, now())"""
    db.session.execute(
        text(sql), {"username": username, "password": hash_value, "admin": False}
    )
    db.session.commit()


def add_visit(usr_id):
    sql = "INSERT INTO visits (user_id, time) VALUES (:user_id, now())"
    db.session.execute(text(sql), {"user_id": usr_id})
    db.session.commit()


def login(username, password):
    user = get_user(username)
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["admin"] = user.admin
        session["csrf_token"] = token_hex(16)
        add_visit(user.id)
        return True
    return False


def delete_session():
    del session["user_id"]
    del session["username"]
    del session["admin"]
    del session["csrf_token"]


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        exec_register(username, hash_value)
    except Exception as err:
        print(err)
        return False
    return login(username, password)


def user_id():
    return session.get("user_id", 0)


def current_user():
    return session.get("username", None)


def is_admin():
    return session.get("admin", False)


def password_valid(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,20}$"

    pattern = re.compile(reg)
    valid = re.search(pattern, password)

    # validating conditions
    return valid
