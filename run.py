from flask import Flask, render_template, jsonify
from forms import SearchForm
from get_data import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "2018"
# SECRET_KEY = '2018'

highest_distances = {}
highest = 0


counties_info = []
for x in counties_waterpoints:
    counties_info.append({"name":x, "population": counties_waterpoints[x]})



@app.route("/")
def index():
    #return json.JSONEncoder(waterpoints)
    #return render_template("index.html")
    searchForm = SearchForm()
    number_of_counties = len(all_counties)
    number_of_waterpoints = len(all_waterpoints)
    print(counties_waterpoints)
    for x in counties_waterpoints:
        print(counties_waterpoints[x])
    return render_template('index.html', points={"data":known_waterpoints},
        number_of_counties=number_of_counties, number_of_waterpoints=number_of_waterpoints,
        total_population = total_population, counties_waterpoints=counties_info,
        number_of_wards=len(all_wards), searchForm=searchForm, waterpoint_distances=waterpoints_distances)



@app.route("/waterpoint-info/<waterpoint_id>")
def waterpoint_info(waterpoint_id):
    waterpoint = None

    searchForm = SearchForm()
    for point in all_waterpoints:
        if point["id"] == int(waterpoint_id):
            waterpoint = point
            break
    if waterpoint == None:
        return render_template("waterpoint_not_found.html")
    return render_template("waterpoint_info.html", waterpoint_data=waterpoint, searchForm=searchForm)


@app.route("/basic-tables")
def basic_tables():
    searchForm = SearchForm()
    return render_template("tables-basic.html", waterpoints_distances=waterpoints_distances,
    id_name_mapping=id_name_mapping, searchForm=searchForm)


@app.route('/data-tables')
def data_tables():
    return render_template("tables-data.html")


@app.route('/google-maps')
def google_maps():
    central_point_json = {"central_point": central_point}
    searchForm = SearchForm()
    # all_waterpoints = all_waterpoints
    # all_waterpoint_locations = all_waterpoint_locations
    return render_template("maps-gmap.html", central_point_json=central_point_json,
            all_waterpoint_locations=all_waterpoint_locations, searchForm=searchForm,
            suitable_point=suitable_point)


# @app.route('/')
@app.route('/basic-forms')
def forms_basic():
    return render_template("forms-basic.html")


@app.route('/vector-maps')
def vector_maps():
    return render_template("maps-vector.html")

@app.route('/chart-js')
def chart_js():
    searchForm = SearchForm()
    return render_template("charts-chartjs.html", searchForm=searchForm)

@app.errorhandler(404)
def page_404(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
