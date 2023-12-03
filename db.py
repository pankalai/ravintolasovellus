from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)
