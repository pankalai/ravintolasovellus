import re
import requests
from requests.structures import CaseInsensitiveDict


API_KEY = "94549be1b28d405fbf7d40a5ca43dae6"


class MapService:
    DEFAULT_LATITUDE = 60.16952
    DEFAULT_LONGITUDE = 24.93545

    def __init__(self, api_key):
        self._latitude = self.DEFAULT_LATITUDE
        self._longitude = self.DEFAULT_LONGITUDE
        self._api_key = api_key

    def get_coordinates_for_address(self, address, postcode, city, country="Finland"):
        street, housenumber = self.split_address_to_street_and_housenumber(address)

        if not (housenumber and street):
            return None

        url = (
            "https://api.geoapify.com/v1/geocode/search?"
            + f"housenumber={housenumber}&"
            + f"street={street}&"
            + f"postcode={postcode}&"
            + f"city={city}&"
            + f"country={country}&"
            + f"apiKey={self._api_key}"
        )

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        resp = requests.get(url, headers=headers, timeout=15)

        if resp.status_code == 400:
            return None

        return resp.json()["features"][0]["geometry"]["coordinates"]

    def create_marker(self, res):
        marker = {}

        marker["name"] = res.name
        marker["lat"] = res.location["latitude"]
        marker["lon"] = res.location["longitude"]
        marker["info"] = (
            "<i>"
            + res.description
            + "</i>"
            + "<br>"
            + res.opening_hours.replace("\r", "").replace("\n", ", ")
        )

        return marker

    def get_center_coordinates(self):
        return self._latitude, self._longitude

    def split_address_to_street_and_housenumber(self, address):
        search = re.search(r"\d", address)
        if not search:
            print("Missing housenumber")
            return None, None

        index = search.start()
        street = address[:index].rstrip()
        housenumber = address[index:].split(" ")[0]
        return street, housenumber


map_service = MapService(API_KEY)
