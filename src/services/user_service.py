from secrets import token_hex
import re
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from services.database_service import database_service as db


class UserService:
    def __init__(self):
        pass

    def register(self, username, password1, password2):
        if not self.username_valid(username):
            return False, self.username_requirements

        if password1 != password2:
            return False, "Salasanat eroavat"

        if not self.password_valid(password1):
            return False, self.password_requirements()

        valid, info = self.username_valid(username)
        if not valid:
            return False, info

        hash_value = generate_password_hash(password1)
        try:
            db.add_user(username, hash_value)
        except Exception as err:
            return False, "Rekisteröinti ei onnistunut, yritä myöhemmin uudelleen"

        self.login(username, hash_value)
        return True

    def login(self, username, password):  
        user = db.get_user(username)
        if not user:
            return False, "Tuntematon käyttäjätunnus"
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["admin"] = user.admin
            session["csrf_token"] = token_hex(16)
            self.add_visit(user.id)
            return True, ""
        return False, "Virheellinen salasana"

    def add_visit(self, user_id):
        db.add_visit(user_id)

    def logout(self):
        del session["user_id"]
        del session["csrf_token"]
        del session["username"]
        del session["admin"]

    def username_valid(self, username):
        user = db.get_user(username)
        if user:
            return False, "Tunnus on jo käytössä"
        return True

    def password_valid(self, password):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,20}$"

        pattern = re.compile(reg)
        valid = re.search(pattern, password)

        return valid

    def username_requirements(self):
        return "Tunnuksen tulee olla vähintään kolme merkkiä pitkä"

    def password_requirements(self):
        return """Salasanan tulee täyttää seuraavat ehdot<br><ul><li>
            Yksi pieni kirjain</li><li>Yksi iso kirjain</li><li>Yksi numero</li>
            <li>Pituus vähintään 8 ja korkeintaan 20</li></ul>"""

    def username(self, user_id):
        user = db.get_user(user_id)
        return user.name

    def is_admin(self):
        return session.get("admin", False)



user_service = UserService()
