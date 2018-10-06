from calculations import get_distance
from get_data import waterpoints

waterpoints_info = [] # holds triples of lat, lon and id
waterpoints_distances = {}
# will hold the closest distances to all the waterpoints
# e.g if the closest waterpoint to isiolo->id 1234 is marsabit->id 5678 and the distance is 54.2 km
# it will be:
#   waterpoints_distances  = {
#               '1234': [5678, 54.2]
#}

def get_all_points():
    for point in waterpoints:
        waterpoints_info.append([point['lat'], point['lon'], point['id']])


# this function populates the waterpoints_distances dictionary
# it gets the closest waterpoints to each of the waterpoints that has been mentioneds
def get_closest_points():
    get_all_points()
    for point in waterpoints_info:
        for another_point in waterpoints_info:
            if another_point[2] != point[2]:
                distance = get_distance([point[0], point[1]], [another_point[0], another_point[1]]) # distance between two points in kilometres
                if str(point[2]) not in waterpoints_distances:
                    waterpoints_distances[str(point[2])] = [another_point[2], distance]
                elif distance < waterpoints_distances[ str(point[2]) ][1]:
                    waterpoints_distances[str(point[2])] = [another_point[2], distance]


# gets the average distance between each of the waterpoints that have been mentioned 
def get_average_closest_distance():
    get_closest_points()
    points = []
    for distance in waterpoints_distances:
        points.append(waterpoints_distances[distance][1])
    counter = 0
    for point in points:
        counter += point
    return (counter / len(points))

print(get_average_closest_distance())
