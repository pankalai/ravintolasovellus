from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")


class Database:
    def __init__(self):
        self._db = SQLAlchemy(app)

    def select(self, sql, data=None):
        try:
            result = self._db.session.execute(text(sql), data)
            return result
        except (IntegrityError, DataError, OperationalError) as error:
            print("An error occurred: ", error)
            self._db.session.rollback()
            return None

    def update(self, sql, data=None, commit=True, return_value=False):
        try:
            result = self._db.session.execute(text(sql), data)
            if commit:
                self.commit()
        except (IntegrityError, DataError, OperationalError) as error:
            print("An error occurred: ", error)
            self._db.session.rollback()
            return False

        if return_value:
            return result
        return True

    def commit(self):
        try:
            self._db.session.commit()
        except (IntegrityError, DataError, OperationalError) as error:
            print("An error occurred: ", error)
            self._db.session.rollback()
            return False
        return True


db = Database()
