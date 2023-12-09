import json
from flask import render_template, redirect, request, url_for, session, abort
from app import app


from services.map_service import map_service as map_s
from services.user_service import user_service as user_s
from services.restaurant_service import restaurant_service as res_s
from services.category_service import category_service as cat_s
from services.rating_service import rating_service as rat_s



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success, info = user_s.login(username, password)
        if success:
            return redirect("/")
        else:
            return render_template("login.html", notice=info)
    return render_template("login.html")


@app.route("/logout")
def logout():
    user_s.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", info=user_s.password_requirements())
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        success, info = user_s.register(username, password1, password2)
        if not success:
            return render_template(
                "register.html",
                notice=info,
            )

    return redirect("/")







