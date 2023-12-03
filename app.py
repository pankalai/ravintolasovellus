from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
API_KEY = "94549be1b28d405fbf7d40a5ca43dae6"

import routes
