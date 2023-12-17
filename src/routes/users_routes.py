from flask import render_template, redirect, request
from app import app

from services.user_service import user_service as user_s


@app.route("/")
def index(error=None):
    user_id = user_s.get_user_id()
    last_visit = None
    if user_id:
        last_visit = user_s.get_last_visit(user_id)
    return render_template("index.html", last_visit=last_visit, error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        info = user_s.login(username, password)
    return index(info)


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

        info = user_s.register(username, password1, password2)

        if info:
            return render_template(
                "register.html",
                notice=info,
            )

    return redirect("/")
