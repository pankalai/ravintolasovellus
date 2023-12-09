from flask import render_template, redirect, request, url_for, session, abort
from app import app

from services.map_service import map_service as map_s
from services.user_service import user_service as user_s
from services.restaurant_service import restaurant_service as res_s
from services.category_service import category_service as cat_s
from services.rating_service import rating_service as rat_s

@app.route("/ratings")
def show_ratings():
    rat = rat_s.get_ratings()
    cat = cat_s.get_categories()
    session["previous_url"] = url_for("show_ratings")
    return render_template(
        "ratings.html", ratings=rat, categories=cat, entity="ratings"
    )


@app.route("/ratings/search", methods=["POST"])
def search_ratings():
    sel_cat, city, search_text, cat = form_s.get_info_for_search_form(request)

    rat = ratings.get_ratings(sel_cat, city, search_text)

    return render_template(
        "ratings.html",
        ratings=rat,
        selected_categories=sel_cat,
        categories=cat,
        city=city,
        search_text=search_text,
        entity="ratings",
    )


@app.route("/ratings/send", methods=["POST"])
def send_rating():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    restaurant_id = request.form.get("id")
    stars = request.form.get("stars")
    comment = request.form.get("comment")
    ratings.add_rating(user_s.user_id(), restaurant_id, stars, comment)
    return redirect("/ratings")


@app.route("/ratings/new/<int:restaurant_id>")
def new_rating(restaurant_id):
    res = res_s.get_restaurant(restaurant_id)
    return render_template("ratings_new.html", id=id, restaurant=res)


@app.route("/ratings/<int:rating_id>/delete", methods=["POST"])
def hide_rating(rating_id):
    if session["csrf_token"] != request.form["csrf_token"] or not user_s.is_admin():
        abort(403)
    ratings.hide_rating(rating_id)
    re_id = request.form["restaurant_id"]
    return redirect("/restaurants/" + re_id + "/ratings")