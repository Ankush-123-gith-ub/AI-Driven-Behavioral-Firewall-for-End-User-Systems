from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

LOG_FILE = os.path.join("storage", "events_log.json")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def get_data():
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data[-10:])
    except:
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)