from services.database_service import database_service as db

class RatingService:
    def get_ratings(self):
        return db.get_ratings()

    def get_restaurants_ratings(self, restaurant_id):
        return db.get_restaurants_ratings(restaurant_id)

rating_service = RatingService()