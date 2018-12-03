from flask import Flask, render_template
import pandas as pd
import polyline
import requests
import json

app = Flask(__name__, template_folder='templates')

class_df = pd.read_csv("fall18.csv")
building_df = pd.read_csv("building_data.csv")


@app.route('/')
def root():
    return app.send_static_file('html/index.html')


@app.route('/<int:class_id_1>/<int:class_id_2>/')
def process_class_id(class_id_1=None, class_id_2=None):

    # Get building IDs
    class_1_building = class_df.loc[class_df['code'] == class_id_1]["building"].values[0]
    class_2_building = class_df.loc[class_df['code'] == class_id_2]["building"].values[0]

    # Get building addresses
    class_1_address = building_df.loc[building_df['code'] == class_1_building]["address"].values[0]
    class_2_address = building_df.loc[building_df['code'] == class_2_building]["address"].values[0]

    # Craft request to Google Maps API
    url = "https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1} + " \
          "&key=AIzaSyCDXE6q_zHm19AprJL4CvHn-HkNbaFMDro&mode=walking".format(class_1_address, class_2_address)

    # Get only the data needed from API resopnse
    data = requests.get(url).json()["routes"][0]["legs"][0]

    coordinates = []

    # Iterate through response data, adding the start location of each "move"
    for i in data["steps"]:
        coordinates.append((i["start_location"]["lat"], i["start_location"]["lng"]))

    # Append the end location (we didn't get end locations in the above loop)
    end_location = (data["end_location"]["lat"],
                    data["end_location"]["lng"])
    coordinates.append(end_location)

    # Encode polyline, create URL
    encoded_polyline = polyline.encode(coordinates)
    static_map_url = "https://maps.googleapis.com/maps/api/staticmap?size=400x400" + \
                     "&key=AIzaSyCDXE6q_zHm19AprJL4CvHn-HkNbaFMDro&path=enc:{0}".format(encoded_polyline)

    return render_template('map.html', map_url=static_map_url)
