import requests
import json
from calculations import get_distance
from statistics import variance
import pandas as pd
import statistics as st
import numpy as np
#req = requests.get("https://kenya-rapid-app-server-dev.mybluemix.net/waterpoints")
#json_data = req.json()

json_file = open("data.json", "r")
json_data = json_file.read()
json_data = json.loads(json_data)
lats = []
lons = []

all_waterpoints = [] # lists all waterpoints available
all_waterpoint_locations = []
all_counties = [] # lists all the counties that have been covered during this analysis
total_population = 0 # gets the total number of people being covered
unknown_waterpoints = [] # lists all the waterpoints whose locations we don't have
known_waterpoints = [] # has a list of all the waterpoints in which we have the location of
distances = [] # has the all the closest distances to all the waterpoints, unseived
inactive = 0
active = 0
counties_waterpoints = {}
all_wards = []
central_point = []
id_name_mapping = {}
# waterpoints_distances = {}

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
        if x['lon'] > 37.60305827189648 and x['lat'] > 0.3610877866467687:
            known_waterpoints.append(x)
    else:
        unknown_waterpoints.append(x)
    all_waterpoints.append(x)


for x in known_waterpoints:
    # all_waterpoint_locations.append([x["id"], x["lon"], x["lat"], x["name"]])
    # print(x["id"])
    data = {}
    if "name" in x:
        data["id"] = x["id"]
        data["lat"] = x["lat"]
        data["lon"] = x["lon"]
        data["name"]= x["name"]
        # all_waterpoint_locations.append([x["lat"], x["lon"], x["name"], x["id"]])
    all_waterpoint_locations.append(data)


for point in all_waterpoints:
    if 'id' in point and 'name' in point:
        id_name_mapping[point['id']] = point['name']

# print(id_name_mapping)
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
    for point in known_waterpoints:
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

get_closest_waterpoints()
# print(all_waterpoints)

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


def get_number_of_counties():
    for point in all_waterpoints:
        if 'county' in point and point['county']['name'] not in all_counties:
            all_counties.append(point['county']['name'])

        if 'county' in point and point['county']['name'] not in counties_waterpoints:
            counties_waterpoints[point['county']['name']] = 1
        elif 'county' in point and point['county']['name'] in counties_waterpoints:
            counties_waterpoints[point['county']['name']] += 1

    return None

def get_population():
    population = 0
    for point in all_waterpoints:
        if 'waterpointUsage' in point and 'people' in point['waterpointUsage']:
            population += point['waterpointUsage']['people']
    return population
# print(get_central_point())
# print(get_cost_per_liter())


def get_all_wards():
    for point in all_waterpoints:
        if 'ward' in point and point['ward']['name'] not in all_wards:
            all_wards.append( point['ward']['name'] )


def reduce_datapoints_distances():
    lats = []
    lons = []
    for point in all_waterpoint_locations:
        lats.append(point["lat"])

    for point in all_waterpoint_locations:
        lons.append(point["lon"])

    # print(st.variance(lons))
    # print(st.variance(lats))

reduce_datapoints_distances()
total_population += get_population()
get_number_of_counties()
get_all_wards()
central_point = get_central_point()
get_active_waterpoints()
get_closest_waterpoints()

# for x in all_waterpoint_locations:
#     print(x)
#     print("############")



for waterpoint in known_waterpoints:
    lons.append(waterpoint['lon'])
    lats.append(waterpoint['lat'])
    # print(known_waterpoints[waterpoint])

lons.sort()
lats.sort()


lonArr = np.array(lons)     # creates a numpy array for the longitudes
latArr = np.array(lats)     # creates a numpy array for the latitudes

lonDiff = np.diff(lonArr)   # creates a numpy array with the differences of all the longitudes
latDiff = np.diff(latArr)   # creates a numpy array with the differences of all the latitudes

max_lonDiff = max(lonDiff)  # largest difference in the longitudes (disparity in longitudes between the waterpoints)
max_latDiff = max(latDiff)  # largest difference in the latitudes (disparity in latitudes between the waterpoints)

lon_index = np.where(lonDiff==max_lonDiff)[0][0]
lat_index = np.where(latDiff==max_latDiff)[0][0]


lon_disp = (lonArr[lon_index] + lonArr[lon_index - 1]) / 2
lat_disp = (latArr[lat_index] + latArr[lat_index - 1]) / 2

suitable_point = [lat_disp, lon_disp]

# print(waterpoints_distances)
