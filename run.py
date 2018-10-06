from flask import Flask, render_template, json
from get_data import waterpoints

app = Flask(__name__)

@app.route("/")
def index():
    #return json.JSONEncoder(waterpoints)
    #return render_template("index.html")
    return str(waterpoints)
    
if __name__ == "__main__":
    app.run(debug=True)
