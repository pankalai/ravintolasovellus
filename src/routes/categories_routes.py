from flask import render_template, redirect, request, url_for, session, abort
from app import app

from services.user_service import user_service as user_s
from services.category_service import category_service as cat_s


@app.route("/categories")
def show_categories():
    if not user_s.is_admin():
        abort(403)
    notice = request.args.get('notice')
    categories = cat_s.get_categories_and_restaurants()
    return render_template("categories.html", categories=categories, notice=notice)


@app.route("/categories/add", methods=["POST"])
def add_category():
    if session["csrf_token"] != request.form["csrf_token"] or not user_s.is_admin():
        abort(403)
    name = request.form.get("name")
    info = cat_s.add_category(name)
    return redirect(url_for('.show_categories', notice=info))


@app.route("/categories/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):
    cat_s.delete_category(category_id)
    return redirect("/categories")
