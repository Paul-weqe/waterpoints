from math import sin, cos, sqrt, atan2, radians

R = 6373.0 # radius of the earth (apparently)

def get_distance(coordinates1, coordinates2):
    lat1 = radians(coordinates1[0])
    lon1 = radians(coordinates1[1])

    lat2 = radians(coordinates2[0])
    lon2 = radians(coordinates2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    distance = R * c
    return distance
