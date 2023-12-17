from datetime import datetime

from services.database_service import database_service as db
from services.user_service import user_service as user_s


class RatingService:

    def get_ratings(self, category=None, city=None, word=None):
        return db.get_ratings(category, city, word)

    def get_restaurants_ratings(self, restaurant_id):
        return db.get_restaurants_ratings(restaurant_id)

    def add_rating(self, restaurant_id, stars, comment):
        user_id = user_s.get_user_id()

        if user_id:
            last_rating = db.get_rating_by_restaurant_and_user(user_id, restaurant_id)

            if last_rating:
                if (datetime.now()-last_rating).days == 0:
                    return "Olet jo antanut arvion ravintolasta tänään"

            if not db.add_rating(user_id, restaurant_id, stars, comment):
                return "Arvion lisääminen epäonnistui"

        return None

    def hide_rating(self, rating_id):
        if not db.hide_rating(rating_id):
            return False, "Arvion poistaminen epäonnistui"
        return True, "Arvio poistettiin"



rating_service = RatingService()
