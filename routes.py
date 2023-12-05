import json
from flask import render_template, redirect, request, url_for, session, abort
from app import app

import users
import map
import categories
import ratings
import restaurants


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
            return render_template(
                "register.html",
                notice="Salasanat eroavat",
            )
        if not users.password_valid(password1):
            return render_template(
                "register.html",
                notice=users.get_password_requirements(),
            )
        if users.register(username, password1):
            return redirect("/")
        return render_template(
            "register.html",
            notice="Rekisteröinti ei onnistunut. Yritä myöhemmin uudelleen.",
        )
    return render_template("register.html")


# Restaurants


@app.route("/restaurants")
def restaurant():
    return redirect("/restaurants/list")


@app.route("/restaurants/<string:list_type>")
def show_restaurants(list_type):
    if list_type == "list":
        res = restaurants.get_restaurants()
        cat = categories.get_categories()
        session["previous_url"] = url_for("restaurant")
        return render_template("restaurants_list.html", restaurants=res, categories=cat)
    if list_type == "map":
        markers = map.create_markers(restaurants.get_restaurants())
        user_coordinates = map.get_user_coordinates()
        return render_template(
            "restaurants_map.html",
            user_lat=user_coordinates[0],
            user_lon=user_coordinates[1],
            markers=markers,
        )
    return redirect("/restaurants")


@app.route("/restaurants/search", methods=["POST"])
def restaurants_search():
    categories_selected = request.form.getlist("categories", None)
    city = request.form.get("city", None)
    search_text = request.form.get("description", None)

    res = restaurants.get_restaurants(categories_selected, city, search_text)
    cat = categories.get_categories()

    return render_template(
        "restaurants_list.html",
        restaurants=res,
        categories=cat,
        selected_categories=[int(c) for c in categories_selected],
        city=city,
        search_text=search_text,
    )


@app.route("/restaurant/new")
def add_restaurant():
    if not users.is_admin():
        abort(403)
    cat = categories.get_categories()
    return render_template("restaurant_form.html", restaurant={}, categories=cat)


@app.route("/restaurants/<int:restaurant_id>/edit")
def edit_restaurant(restaurant_id):
    if not users.is_admin():
        abort(403)
    res = restaurants.get_restaurant(restaurant_id)
    res = res._asdict()
    cat = categories.get_categories()
    res_cat = categories.get_restaurant_category(restaurant_id)

    res_cat = [int(item.id) for item in res_cat]
    return render_template(
        "restaurant_form.html",
        restaurant=res,
        categories=cat,
        restaurant_category=res_cat,
    )


@app.route("/restaurant/send", methods=["POST"])
def restaurant_send():
    if session["csrf_token"] != request.form["csrf_token"] or not users.is_admin():
        abort(403)

    restaurant_id = None if request.form["id"] == "None" else request.form["id"]
    name = request.form["name"].lstrip().rstrip()
    description = request.form.get("description").lstrip().rstrip()
    opening_hours = request.form.get("opening_hours").lstrip().rstrip()
    cats = request.form.getlist("categories")

    location = {}
    for i in ["street", "zip", "city"]:
        location[i] = request.form.get(i).lstrip().rstrip()

    old_info = None if request.form["old_info"] == "None" else request.form["old_info"]

    # Missing info check
    if not (
        name
        and location["street"]
        and location["zip"]
        and location["city"]
        and opening_hours
    ):
        res = (
            json.loads(request.form["old_info"].replace("'", '"')) if old_info else None
        )
        return render_template(
            "restaurant_form.html",
            restaurant=res,
            notice="Lähetys ei onnistunut, tietoja puuttuu",
        )

    # Missing coordinates check
    get_coordinates = False
    if not restaurant_id:
        get_coordinates = True
    else:
        old_info = old_info.replace("'", '"')
        old_info = json.loads(old_info)

        if (
            not old_info["location"].get("latitude")
            or not old_info["location"].get("longitude")
            or not (
                old_info["location"]["street"] == location["street"]
                and old_info["location"]["zip"] == location["zip"]
                and old_info["location"]["city"] == location["city"]
            )
        ):
            get_coordinates = True

    if get_coordinates:
        street, housenumber = map.split_address_to_street_and_housenumber(
            location["street"]
        )
        coordinates = map.get_coordinates_for_address(
            street, housenumber, location["zip"], location["city"]
        )
        if coordinates:
            location["longitude"] = coordinates[0]
            location["latitude"] = coordinates[1]

    if not restaurant_id:
        restaurants.add_restaurant(name, description, location, opening_hours, cats)
    else:
        restaurants.update_restaurant(
            restaurant_id, name, description, location, opening_hours, cats
        )
    return redirect("/restaurants/list")


@app.route("/restaurants/<int:restaurant_id>/ratings")
def show_restaurant_ratings(restaurant_id):
    res = restaurants.get_restaurant(restaurant_id, True)
    if not res:
        return redirect("/ratings")
    rat = ratings.get_restaurants_ratings(restaurant_id)
    return render_template("restaurant_ratings.html", ratings=rat, res=res)


@app.route("/restaurants/<int:restaurant_id>")
def show_restaurant(restaurant_id):
    res = restaurants.get_restaurant(restaurant_id, True)
    if not res:
        return redirect("/restaurants/list")
    cat = categories.get_restaurant_category(restaurant_id)

    return render_template("restaurant.html", restaurant=res, categories=cat)


@app.route("/restaurants/<int:restaurant_id>/delete", methods=["POST"])
def restaurant_delete(restaurant_id):
    if session["csrf_token"] != request.form["csrf_token"] or not users.is_admin():
        abort(403)
    restaurants.hide_restaurant(restaurant_id)
    return redirect("/restaurants/list")


# Ratings


@app.route("/ratings")
def show_ratings():
    rat = ratings.get_ratings()
    cat = categories.get_categories()
    session["previous_url"] = url_for("show_ratings")
    return render_template("ratings.html", ratings=rat, categories=cat)


@app.route("/ratings/search", methods=["POST"])
def search_ratings():
    categories_selected = request.form.getlist("categories", None)
    city = request.form.get("city", None)
    rat = ratings.get_ratings(categories_selected, city)
    cat = categories.get_categories()
    session["previous_url"] = url_for("show_ratings")
    return render_template(
        "ratings.html",
        ratings=rat,
        selected_categories=[int(c) for c in categories_selected],
        categories=cat,
        city=city,
    )


@app.route("/ratings/send", methods=["POST"])
def send_rating():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    restaurant_id = request.form.get("id")
    stars = request.form.get("stars")
    comment = request.form.get("comment")
    ratings.add_rating(users.user_id(), restaurant_id, stars, comment)
    return redirect("/ratings")


@app.route("/ratings/new/<int:restaurant_id>")
def new_rating(restaurant_id):
    res = restaurants.get_restaurant(restaurant_id)
    return render_template("ratings_new.html", id=id, restaurant=res)


@app.route("/ratings/<int:rating_id>/delete", methods=["POST"])
def hide_rating(rating_id):
    if session["csrf_token"] != request.form["csrf_token"] or not users.is_admin():
        abort(403)
    ratings.hide_rating(rating_id)
    re_id = request.form["restaurant_id"]
    return redirect("/restaurants/" + re_id + "/ratings")


# Categories


@app.route("/categories")
def show_categories():
    if not users.is_admin():
        abort(403)
    cats = categories.get_categories_and_restaurants()
    cat = {}
    for ca in cats:
        if ca.name not in cat:
            cat[ca.name] = {}
            cat[ca.name]["count"] = 0
            cat[ca.name]["restaurants"] = []
        if ca.restaurant:
            cat[ca.name]["count"] += 1
            cat[ca.name]["restaurants"].append((ca.restaurant, ca.city))

    return render_template("categories.html", categories=cat)


@app.route("/categories/add", methods=["POST"])
def add_category():
    if session["csrf_token"] != request.form["csrf_token"] or not users.is_admin():
        abort(403)
    name = request.form.get("name")
    categories.add_category(name)
    return redirect("/categories")
