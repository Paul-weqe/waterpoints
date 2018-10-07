import requests
import json
from calculations import get_distance
from statistics import variance
#req = requests.get("https://kenya-rapid-app-server-dev.mybluemix.net/waterpoints")
#json_data = req.json()

json_file = open("data.json", "r")
json_data = json_file.read()
json_data = json.loads(json_data)

all_waterpoints = [] # lists all waterpoints available
unknown_waterpoints = [] # lists all the waterpoints whose locations we don't have
known_waterpoints = [] # has a list of all the waterpoints in which we have the location of
distances = [] # has the all the closest distances to all the waterpoints, unseived
inactive = 0
active = 0


waterpoints_info = [] # holds triples of lat, lon and id
waterpoints_distances = {}
""" will hold the closest distances to all the waterpoints
 e.g if the closest waterpoint to isiolo->id 1234 is marsabit->id 5678 and the distance is 54.2 km
 it will be:


waterpoints_distances  = {
               '1234': [5678, 54.2]
}
"""


# adds to the waterpoints list only the points in which we have the longitude and latitude
for x in json_data["data"]:
    if 'lon' in x and 'lat' in x:
        known_waterpoints.append(x)
    else:
        unknown_waterpoints.append(x)
    all_waterpoints.append(x)


waterpoint_quality = {
    'good': 0,
    'bad': 0,
} # holds the quality ('good' or 'bad') and the number of places that have this data
# populates the waterpoint_quality dictionary
for waterpoint in all_waterpoints:
    if 'waterquality' in waterpoint:
        if waterpoint['waterquality'].lower() == 'bad':
            waterpoint_quality['bad'] = waterpoint_quality['bad'] + 1
        elif waterpoint['waterquality'].lower() == 'good':
            waterpoint_quality['good'] = waterpoint_quality['good'] + 1

# get active points of the waterpoints
def get_active_waterpoints():
    active = 0
    inactive = 0
    for point in all_waterpoints:
        if 'status' in point:
            if point['status'] != 'active':
                inactive += 1
            else:
                active += 1
    return active

# adds all the known point's information to the waterpoints_info list
# this will be useful later...you'll see
def get_all_known_points():
    for point in waterpoints:
        waterpoints_info.append([point['lat'], point['lon'], point['id']])


# this function populates the waterpoints_distances dictionary
# it gets the closest waterpoints to each of the waterpoints that has been mentioneds
def get_closest_waterpoints():
    get_all_known_points()
    for point in waterpoints_info:
        for another_point in waterpoints_info:
            if another_point[2] != point[2]: # we are not looking at the same point for 'point' and 'another_point' variables
                distance = get_distance([point[0], point[1]], [another_point[0], another_point[1]]) # distance between two points in kilometres
                if str(point[2]) not in waterpoints_distances:
                    waterpoints_distances[str(point[2])] = [another_point[2], distance]
                elif distance < waterpoints_distances[ str(point[2]) ][1]:
                    waterpoints_distances[str(point[2])] = [another_point[2], distance]


# gets the average distance between each of the waterpoints that have been mentioned
def get_average_closest_distance():
    get_closest_waterpoints()
    for distance in waterpoints_distances:
        distances.append(waterpoints_distances[distance][1])
    counter = 0
    for distance in distances:
        counter += distance
    return (counter / len(distances))

def get_central_point():
    lats = []
    lons = []
    for point in known_waterpoints:
        lats.append(point['lat'])
        lons.append(point['lon'])

    lat_mean = sum(lats) / float(len(lats))
    lon_mean = sum(lons) / float(len(lons))

    return ([lat_mean, lon_mean])
# counter = 0
def get_cost_per_liter():
    # counter = 0
    cost = {}
    for waterpoint in all_waterpoints:
        if "waterpointCost" in waterpoint:
            for cost_type in waterpoint['waterpointCost']:
                if cost_type in cost and (cost_type != "date" and cost_type != "id"):
                    cost[cost_type].append(waterpoint['waterpointCost'][cost_type])
                elif cost_type not in cost and (cost_type != "date" and cost_type != "id"):
                    cost[cost_type] = []
                    cost[cost_type].append(waterpoint['waterpointCost'][cost_type])
    # print(cost)
    return cost

types = []
def get_usage_types():
    for point in all_waterpoints:
        if 'waterpointUsage' in point:
            for usage_type in point['waterpointUsage']:
                if usage_type not in types:
                    types.append(usage_type)

get_usage_types()
print(types)
# print(get_central_point())
# print(get_cost_per_liter())
