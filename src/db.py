from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import exc
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)

# class Database:
#     def execute_command(self):
#         try:
#             pass
#         except Exception as error:
#             print("Tapahtui virhe: ", error)
#             database.session.rollback()
#             return False
#         return True



# db = Database()