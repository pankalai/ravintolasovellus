import re
import requests
from requests.structures import CaseInsensitiveDict
from app import API_KEY
import restaurants


def get_coordinates_for_address(street, housenumber, postcode, city, country="Finland"):
    url = (
        "https://api.geoapify.com/v1/geocode/search?"
        + f"housenumber={housenumber}&"
        + f"street={street}&"
        + f"postcode={postcode}&"
        + f"city={city}&"
        + f"country={country}&"
        + f"apiKey={API_KEY}"
    )

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers, timeout=15)

    if resp.status_code == 400:
        return None

    return resp.json()["features"][0]["geometry"]["coordinates"]


def create_markers(rest: list):
    markers = []
    for res in rest:
        marker = {}
        if not res.location.get("latitude") or not res.location.get("longitude"):
            street, housenumber = split_address_to_street_and_housenumber(
                res.location["street"]
            )
            postcode = res.location["zip"]
            city = res.location["city"]

            if not (housenumber and street and postcode and city):
                continue

            # print("Haetaan koordinaatit", res.location)
            coordinates = get_coordinates_for_address(
                street, housenumber, postcode, city
            )

            if not coordinates:
                continue

            lon = coordinates[0]
            lat = coordinates[1]

            # Update restaurant's info in database
            res.location["latitude"] = lat
            res.location["longitude"] = lon
            restaurants.update_restaurant(
                res.id,
                res.name,
                res.description,
                res.location,
                res.opening_hours,
            )

        else:
            lat = res.location["latitude"]
            lon = res.location["longitude"]

        marker["name"] = res.name
        marker["lat"] = lat
        marker["lon"] = lon
        marker["info"] = (
            "<i>"
            + res.description
            + "</i>"
            + "<br>"
            + res.opening_hours.replace("\r", "").replace("\n", ", ")
        )

        markers.append(marker)

    return markers


def get_user_coordinates():
    latitude = 60.16952
    longitude = 24.93545
    return latitude, longitude


def split_address_to_street_and_housenumber(address):
    try:
        index = re.search(r"\d", address).start()
        street = address[:index].rstrip()
        housenumber = address[index:].split(" ")[0]
        return street, housenumber
    except:
        return None, None
