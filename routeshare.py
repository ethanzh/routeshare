from flask import Flask, render_template
import pandas as pd
from helper_methods import create_map_image

app = Flask(__name__)

# Pandas DataFrame containing all course information
class_df = pd.read_csv("fall18.csv")


@app.route('/<string:building_1>/<string:building_2>/')
def process_building_names(building_1=None, building_2=None):

    static_map_url = create_map_image(building_1, building_2)

    return render_template('map.html', map_url=static_map_url)


@app.route('/<int:class_id_1>/<int:class_id_2>/')
def process_class_id(class_id_1=None, class_id_2=None):
    # Get building IDs
    building_1 = class_df.loc[class_df['code'] == class_id_1]["building"].values[0]
    building_2 = class_df.loc[class_df['code'] == class_id_2]["building"].values[0]

    static_map_url = create_map_image(building_1, building_2)

    return render_template('map.html', map_url=static_map_url)
