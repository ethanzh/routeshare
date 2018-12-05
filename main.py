from flask import Flask, render_template, jsonify
import pandas as pd
from helper_methods import two_lines, get_overlap

app = Flask(__name__)

# Pandas DataFrame containing all course information
class_df = pd.read_csv("fall18.csv")


@app.route('/')
def home_page():
    return app.send_static_file("html/index.html")


@app.route('/<string:building_1>/<string:building_2>/to/<string:building_3>/<string:building_4>/')
def process_four_buildings(building_1=None, building_2=None, building_3=None, building_4=None):

    map_url = two_lines(building_1, building_2, building_3, building_4)
    shared_url = get_overlap(building_1, building_2, building_3, building_4)

    return jsonify(
        map_url=map_url,
        shared_url=shared_url
    )
