from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import exc
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")


class Database:
    def __init__(self):

        self._db = SQLAlchemy(app)

    def select(self, sql, data=None):
        try:
            result = self._db.session.execute(text(sql), data)
            return result
        except Exception as error:
            print("An error occurred: ", error)
            database.session.rollback()
            return None

    def update(self, sql, data=None, commit=True, return_value=False):
        try:
            result = self._db.session.execute(text(sql), data)
            if commit:
                self.commit()
        except Exception as error:
            print("An error occurred: ", error)
            self._db.session.rollback()
            return False
        
        if return_value:
            return result
        return True

    def commit(self):
        try:
            self._db.session.commit()
        except Exception as error:
            print("An error occurred: ", error)
            self._db.session.rollback()
            return False
        return True


db = Database()
