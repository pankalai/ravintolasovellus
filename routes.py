import json
from flask import render_template, redirect, request, url_for, session, abort
from app import app
import users
import db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Väärä tunnus tai salasana")
    return render_template("login.html")


@app.route("/logout")
def logout():
    users.delete_session()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        return render_template("error.html", message="Rekisteröinti ei onnistunut")
    return render_template("register.html")


# Restaurants


@app.route("/restaurants")
def restaurant():
    return redirect("/restaurants/list")


@app.route("/restaurants/<string:list_type>")
def restaurants(list_type):
    if list_type == "list":
        res = db.get_restaurants()
        res = sorted(res, key=lambda r: r.name)
        session["previous_url"] = url_for("restaurant")
        return render_template("restaurants_list.html", restaurants=res)
    return render_template("restaurants_" + list_type + ".html")


@app.route("/restaurants/search", methods=["POST"])
def restaurants_search():
    category = request.form.get("category", None)
    city = request.form["city"]
    description = request.form["description"]
    res = db.get_restaurants(category, city, description)
    return render_template("restaurants_list.html", restaurants=res)


@app.route("/restaurants/send", methods=["POST"])
def restaurant_send():
    if session["csrf_token"] != request.form["csrf_token"] or not users.admin():
        abort(403)
    restaurant_id = request.form["id"] if "id" in request.form.keys() else None
    name = request.form["name"]
    description = request.form.get("description")

    location = {}
    for i in ["street", "zip", "city"]:
        location[i] = request.form.get(i)

    opening_hours = request.form.get("opening_hours")

    if restaurant_id:
        db.update_restaurant(
            restaurant_id,
            name,
            description,
            json.dumps(location, indent=4),
            opening_hours,
        )
    else:
        db.add_restaurant(
            name,
            description,
            json.dumps(location, indent=4),
            opening_hours,
        )
    return redirect("/restaurants/list")


@app.route("/restaurants/<int:restaurant_id>/ratings")
def show_ratings(restaurant_id):
    rat = db.get_restaurants_ratings(restaurant_id)
    res = db.get_restaurant(restaurant_id)
    rat = sorted(rat, key=lambda r: r.created, reverse=True)
    return render_template("restaurant_ratings.html", ratings=rat, res=res)


@app.route("/restaurants/<int:restaurant_id>")
def show_restaurant(restaurant_id):
    res = db.get_restaurant(restaurant_id)
    return render_template("restaurant.html", restaurant=res)


@app.route("/restaurants/<int:restaurant_id>/edit")
def edit_restaurant(restaurant_id):
    res = db.get_restaurant(restaurant_id)
    return render_template("restaurant_edit.html", restaurant=res)


@app.route("/restaurant/<int:restaurant_id>/delete", methods=["POST"])
def restaurant_delete(restaurant_id):
    if session["csrf_token"] != request.form["csrf_token"] or not users.admin():
        abort(403)
    db.hide_restaurant(restaurant_id)
    return redirect("/restaurants/list")


# Ratings


@app.route("/ratings")
def ratings():
    rat = db.get_ratings()
    rat = sorted(rat, key=lambda r: r.average, reverse=True)
    session["previous_url"] = url_for("ratings")
    return render_template("ratings.html", ratings=rat)


@app.route("/ratings/search", methods=["POST"])
def ratings_search():
    category = request.form.get("category", None)
    city = request.form.get("city", None)
    rat = db.get_ratings(category, city)
    rat = sorted(rat, key=lambda r: r.average, reverse=True)
    session["previous_url"] = url_for("ratings")
    return render_template("ratings.html", ratings=rat)


@app.route("/ratings/send", methods=["POST"])
def rating_send():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    restaurant_id = request.form.get("id")
    stars = request.form.get("stars")
    comment = request.form.get("comment")
    db.add_rating(users.user_id(), restaurant_id, stars, comment)
    return redirect("/ratings")


@app.route("/ratings/new/<int:restaurant_id>")
def ratings_new(restaurant_id):
    res = db.get_restaurant(restaurant_id)
    return render_template("ratings_new.html", id=id, restaurant=res)


@app.route("/ratings/<int:rating_id>/delete", methods=["POST"])
def rating_delete(rating_id):
    if session["csrf_token"] != request.form["csrf_token"] or not users.admin():
        abort(403)
    db.hide_rating(rating_id)
    re_id = request.form["restaurant_id"]
    return redirect("/restaurants/" + re_id + "/ratings")


# Categories


@app.route("/categories")
def show_categories():
    return render_template("categories.html")
