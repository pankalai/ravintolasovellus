from flask import render_template, redirect, request, url_for, session, abort
from app import app

from services.map_service import map_service as map_s
from services.user_service import user_service as user_s
from services.restaurant_service import restaurant_service as res_s
from services.category_service import category_service as cat_s
from services.rating_service import rating_service as rat_s

@app.route("/restaurants")
def restaurant():
    return redirect("/restaurants/list")


@app.route("/restaurants/<string:list_type>")
def show_restaurants(list_type):
    notice = request.args.get("notice")
    all_restaurants = res_s.get_restaurants()
    if list_type == "list":
        categories = cat_s.get_categories()
        session["previous_url"] = url_for("restaurant")
        return render_template(
            "restaurants_list.html",
            restaurants=all_restaurants,
            categories=categories,
            entity="restaurants",
            notice=notice
        )
    if list_type == "map":
        markers = res_s.get_info_for_map()
        center_coordinates = map_s.get_center_coordinates()
        return render_template(
            "restaurants_map.html",
            user_lat=center_coordinates[0],
            user_lon=center_coordinates[1],
            markers=markers,
        )
    return redirect("/restaurants")



@app.route("/restaurant/new")
def add_restaurant():
    if not user_s.is_admin():
        abort(403)
    cat = cat_s.get_categories()
    return render_template("restaurant_new.html", restaurant={}, categories=cat)


@app.route("/restaurants/<int:restaurant_id>")
def show_restaurant(restaurant_id):
    res = res_s.get_restaurant(restaurant_id)
    res = res._asdict()
    cat = cat_s.get_restaurant_categories(restaurant_id)
    pic = res_s.get_image(restaurant_id)
    return render_template("restaurant.html", restaurant=res, categories=cat, image=pic)


@app.route("/restaurants/<int:restaurant_id>/edit")
def edit_restaurant(restaurant_id):
    if not user_s.is_admin():
        abort(403)

    res = res_s.get_restaurant(restaurant_id)
    res = res._asdict()

    all_cat = cat_s.get_categories()

    res_cat = cat_s.get_restaurant_categories(restaurant_id)
    res_cat = [int(item.id) for item in res_cat]

    return render_template(
        "restaurant_edit.html",
        restaurant=res,
        categories=all_cat,
        restaurant_category=res_cat,
    )

@app.route("/restaurants/search", methods=["POST"])
def restaurants_search():
    sel_cat, city, search_text, cat = res_s.get_info_for_search_form(request)
    res = res_s.get_restaurants(sel_cat, city, search_text)

    return render_template(
        "restaurants_list.html",
        restaurants=res,
        selected_categories=sel_cat,
        categories=cat,
        city=city,
        search_text=search_text,
        entity="restaurants",
    )

@app.route("/restaurant/send", methods=["POST"])
def restaurant_send():
    if session["csrf_token"] != request.form["csrf_token"] or not user_s.is_admin():
        abort(403)

    restaurant_id = None if request.form["id"] == "None" else request.form["id"]
    name = request.form["name"].lstrip().rstrip()
    description = request.form.get("description").lstrip().rstrip()
    opening_hours = request.form.get("opening_hours").lstrip().rstrip()
    cats = request.form.getlist("categories")
    street = request.form.get("street").lstrip().rstrip()
    zip_code = request.form.get("zip").lstrip().rstrip()
    city = request.form.get("city").lstrip().rstrip()
    file = request.files.get("file")

    if file:
        res_s.add_image(restaurant_id, file)

    if restaurant_id:
        info = res_s.update_restaurant(
            restaurant_id, name, description, street, zip_code, city, opening_hours, cats
        )
    else:
        info = res_s.add_restaurant(name, description, street, zip_code, city, opening_hours, cats)

    return redirect(url_for(".show_restaurants", list_type="list", notice=info))


@app.route("/restaurants/<int:restaurant_id>/ratings")
def show_restaurant_ratings(restaurant_id):
    res = res_s.get_restaurant(restaurant_id)
    if not res:
        return redirect("/ratings")
    rat = rat_s.get_restaurants_ratings(restaurant_id)
    return render_template("restaurant_ratings.html", ratings=rat, res=res)



@app.route("/restaurants/<int:restaurant_id>/delete", methods=["POST"])
def restaurant_delete(restaurant_id):
    if session["csrf_token"] != request.form["csrf_token"] or not user_s.is_admin():
        abort(403)
    info = res_s.hide_restaurant(restaurant_id)
    return redirect(url_for(".show_restaurants", list_type="list", notice=info))
