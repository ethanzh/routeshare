from flask import Flask, render_template
import pandas as pd
from helper_methods import two_lines

app = Flask(__name__)

# Pandas DataFrame containing all course information
class_df = pd.read_csv("fall18.csv")


@app.route('/')
def home_page():
    return app.send_static_file("html/index.html")

"""
@app.route('/<string:building_1>/<string:building_2>/')
def process_two_buildings(building_1=None, building_2=None):

    static_map_url = create_map_image(building_1, building_2)

    return render_template('map.html', map_url=static_map_url)"""


@app.route('/<string:building_1>/<string:building_2>/to/<string:building_3>/<string:building_4>/')
def process_four_buildings(building_1=None, building_2=None, building_3=None, building_4=None):

    map_url = two_lines(building_1, building_2, building_3, building_4)

    return map_url


"""
@app.route('/<int:class_id_1>/<int:class_id_2>/')
def process_class_id(class_id_1=None, class_id_2=None):
    # Get building IDs
    building_1 = class_df.loc[class_df['code'] == class_id_1]["building"].values[0]
    building_2 = class_df.loc[class_df['code'] == class_id_2]["building"].values[0]

    static_map_url = create_map_image(building_1, building_2)

    return render_template('map.html', map_url=static_map_url)"""

