from math import sin, cos, acos, radians

MEAN_EARTH_RADIUS = 6371.0


def count_distance(latitude_a, longitude_a, latitude_b, longitude_b):
    latitude_a = radians(latitude_a)
    longitude_a = radians(longitude_a)
    latitude_b = radians(latitude_b)
    longitude_b = radians(longitude_b)
    dist_in_radians = acos(
        sin(latitude_a) * sin(latitude_b) + cos(latitude_a) * cos(latitude_b) * cos(longitude_a - longitude_b)
    )
    distance = dist_in_radians * MEAN_EARTH_RADIUS
    return distance
