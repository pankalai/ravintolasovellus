from flask import render_template, request, session, abort
from app import app

from services.user_service import user_service as user_s
from services.category_service import category_service as cat_s


@app.route("/categories")
def show_categories(error=None,success=None):
    if not user_s.is_admin():
        abort(403)
    categories = cat_s.get_categories_and_restaurants()
    return render_template("categories.html", categories=categories, error=error, success=success)


@app.route("/categories/add", methods=["POST"])
def add_category():
    if session["csrf_token"] != request.form["csrf_token"] or not user_s.is_admin():
        abort(403)
    name = request.form.get("name")
    success, info = cat_s.add_category(name)
    if not success:
        return show_categories(info)
    return show_categories(None, info)


@app.route("/categories/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):
    if session["csrf_token"] != request.form["csrf_token"] or not user_s.is_admin():
        abort(403)
    success, info = cat_s.delete_category(category_id)
    if not success:
        return show_categories(info)
    return show_categories(None, info)
