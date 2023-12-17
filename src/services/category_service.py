from services.database_service import database_service as db


class CategoryService:

    def add_category(self, name):
        success = db.add_category(name.capitalize())
        if not success:
            return False, "Kategorian lisääminen epäonnistui"
        return True, "Kategoria lisättiin"

    def delete_category(self, category_id):
        if not db.delete_category(category_id):
            return "Kategorian poistaminen epäonnistui"
        return None

    def get_restaurant_categories(self, restaurant_id):
        return db.get_restaurant_categories(restaurant_id)

    def get_categories(self):
        return db.get_all_columns_from_table("categories", "name")

    def get_categories_and_restaurants(self):
        categories = db.get_categories_and_restaurants(10)
        cats = {}
        for category in categories:
            if category.name not in cats:
                cats[category.name] = {}
                cats[category.name]["id"] = category.id
                cats[category.name]["count"] = category.count
                cats[category.name]["restaurants"] = []
            if category.restaurant:
                cats[category.name]["restaurants"].append(
                    (category.restaurant, category.city)
                )
        return cats


category_service = CategoryService()
