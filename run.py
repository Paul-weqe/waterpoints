from flask import Flask, render_template, jsonify
from get_data import *

app = Flask(__name__)

counties_info = []
for x in counties_waterpoints:
    counties_info.append({"name":x, "population": counties_waterpoints[x]})

@app.route("/")
def index():
    #return json.JSONEncoder(waterpoints)
    #return render_template("index.html")
    number_of_counties = len(all_counties)
    number_of_waterpoints = len(all_waterpoints)
    

    return render_template('index.html', points={"data":known_waterpoints},
        number_of_counties=number_of_counties, number_of_waterpoints=number_of_waterpoints,
        total_population = total_population, counties_waterpoints=counties_info,
        number_of_wards=len(all_wards), )


@app.route("/waterpoint-info/<int:waterpoint_id>")
def waterpoint_info(waterpoint_id):
    waterpoint = None
    for point in all_waterpoints:
        if point["id"] == int(waterpoint_id):
            waterpoint = point
            break
    if waterpoint == None:
        return render_template("waterpoint_not_found.html")
    return render_template("waterpoint_info.html", waterpoint_data=waterpoint)

if __name__ == "__main__":
    app.run(debug=True)
