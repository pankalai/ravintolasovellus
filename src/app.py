from os import getenv
from flask import Flask


app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")


from routes import routes, restaurants_routes, ratings_routes, categories_routes
