# The raw dataset was downloaded from https://prim.iledefrance-mobilites.fr/jeux-de-donnees/emplacement-des-gares-idf-data-generalisee
# and put into data folder.

import math


# def geoloc_trimmer(lat: float, long: float) -> tuple:
#     """
#     Trim the last digits of the geoloc to keep a 100 meters radius, around it.

#     Args:
#         lat (float): The point's latitude.
#         long (float): The point's longitude.

#     Returns:
#         dict: The trimmed geoloc.
#     """
#     lat = round(lat, 4)
#     long = round(long, 4)
#     return (lat, long)


def geoloc_closesness(geoloc_a: dict, geoloc_b: dict) -> bool:
    """
    Caculate the distance between two geoloc, and return true if it is under 500m

    Args:
        geoloc_a (dict: { "lat": float, "long": float}): The geoloc to format.
        geoloc_b (dict: { "lat": float, "long": float}): The geoloc to format.


    Returns:
        bool: True if under 500m, False is more than 500m.
    """
    return (
        math.sqrt(
            (geoloc_a["lat"] - geoloc_b["lat"]) ** 2
            + (geoloc_a["long"] - geoloc_b["long"]) ** 2
        )
        < 0.002
    )


# def is_within_paris(lat: float, long: float) -> bool:
#     # Paris geolocation were check using Google Maps
#     # https://www.google.fr/maps/@lat,long
#     """
#     Check if a point is within Paris.

#     Args:
#         lat (float): The point's latitude.
#         long (float): The point's longitude.

#     Returns:
#         bool: True if the point is within Paris, False otherwise.
#     """
#     return (lat > 48.80 and lat < 48.9) and (long > 2.2 and long < 2.5)
