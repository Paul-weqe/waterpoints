from flask import Flask, render_template, jsonify
from get_data import all_waterpoints, known_waterpoints

app = Flask(__name__)

@app.route("/")
def index():
    #return json.JSONEncoder(waterpoints)
    #return render_template("index.html")
    return render_template('index.html', points={"data":known_waterpoints})


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
