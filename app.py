from os import getenv
from flask import Flask

# from flask_googlemaps import GoogleMaps


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
# app.config["GOOGLEMAPS_KEY"] = getenv("GOOGLEMAPS_KEY")

# GoogleMaps(app)
import routes
