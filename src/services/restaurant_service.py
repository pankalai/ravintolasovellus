from base64 import b64encode

from services.database_service import database_service as db
from services.category_service import category_service as cat_s
from services.map_service import map_service as map_s



class RestaurantService:
    def add_restaurant(self, name, description, street, zip_code, city, opening_hours, cats):
        coordinates = self.get_coordinates(street, zip, city)
        longitude = None if not coordinates else coordinates[0]
        latitude = None if not coordinates else coordinates[1]

        location = self.form_location(street, zip_code, city, longitude, latitude)
        restaurant_id = db.add_restaurant(name, description, location, opening_hours)
        db.add_restaurant_category(restaurant_id, cats)

        if not coordinates:
            return self.missing_coodinates_info(street, zip_code, city)

        return None

    def update_restaurant(self,
            restaurant_id,
            name,
            description,
            street,
            zip_code,
            city,
            opening_hours,
            cats
        ):
        # Location changed check
        old_info = self.get_restaurant(restaurant_id)
        if (
            not old_info.location.get("latitude")
            or not old_info.location.get("longitude")
            or not (
                old_info.location.get("street") == street
                and old_info.location.get("zip") == zip_code
                and old_info.location.get("city") == city
            )
        ):
            coordinates = self.get_coordinates(street, zip_code, city)
            longitude = None if not coordinates else coordinates[0]
            latitude = None if not coordinates else coordinates[1]

        else:
            longitude = old_info.location.get("longitude")
            latitude = old_info.location.get("latitude")

        location = self.form_location(street, zip_code, city, longitude, latitude)
        db.update_restaurant(restaurant_id, name, description, location, opening_hours)
        db.add_restaurant_category(restaurant_id, cats)

        if not (longitude and latitude):
            return self.missing_coodinates_info(street, zip_code, city)

        return None

    def form_location(self, street, zip_code, city, lon=None, lat=None):
        location = {}
        location["street"] = street
        location["zip"] = zip_code
        location["city"] = city
        if lon:
            location["longitude"] = lon
        if lat:
            location["latitude"] = lat
        return location

    def get_info_for_map(self):
        markers = []
        all_restaurants = db.get_restaurants()
        for res in all_restaurants:
            if "latitude" in res.location and "longitude" in res.location:
                marker = map_s.create_marker(res)
                markers.append(marker)

        return markers

    def get_coordinates(self, street, zip_code, city):
        return map_s.get_coordinates_for_address(street, zip_code, city)

    def get_restaurant(self, restaurant_id):
        return db.get_restaurant(restaurant_id)

    def get_restaurants(self, categories=None, city=None, word=None):
        return db.get_restaurants(categories,city,word)

    def get_info_for_search_form(self, request):
        selected_cat = request.form.getlist("categories", None)
        selected_cat = [int(c) for c in selected_cat]
        city = request.form.get("city", None)
        search_text = request.form.get("word", None)
        all_cat = cat_s.get_categories()
        return selected_cat, city, search_text, all_cat

    def hide_restaurant(self, restaurant_id):
        result = db.hide_restaurant(restaurant_id)
        if result:
            return "Ravintola poistettu"
        return "Ravintolan poisto epäonnistui"

    def missing_coodinates_info(self, street, zip_code, city):
        return f"Osoitteelle {street} {zip_code} {city} ei löytynyt koordinaatteja"

    def add_image(self, restaurant_id, file):
        data = file.read()
        name = file.filename

        if len(data) > 100*1024:
            return "Tiedosto on liian iso"

        if not name.endswith(".jpg"):
            return "Virheellinen tiedostomuoto"

        db.delete_image(restaurant_id)
        db.upload_image(restaurant_id, name, data)

        return None

    def get_image(self, restaurant_id):
        result = db.download_image(restaurant_id)
        if not result:
            return None
        image = b64encode(result).decode("utf-8")
        return image


restaurant_service = RestaurantService()
