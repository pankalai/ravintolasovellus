from secrets import token_hex
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import db


def login(username, password):
    user = db.login(username)
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["admin"] = user.admin
        session["csrf_token"] = token_hex(16)
        db.add_visit(user.id)
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
        db.register(username, hash_value)
    except Exception as err:
        print(err)
        return False
    return login(username, password)


def user_id():
    return session.get("user_id", 0)


def current_user():
    return session.get("username", None)


def admin():
    return session["admin"]
