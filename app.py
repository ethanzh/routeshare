from flask import Flask
import pandas as pd
import polyline
import requests

app = Flask(__name__)

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

    data = requests.get(url).json()

    end_location = data["routes"][0]["legs"][0]["end_location"]
    end_location = (end_location["lat"], end_location["lng"])
    data = data["routes"][0]["legs"][0]["steps"]
    coordinates = []
    for i in data:
        start = (i["start_location"]["lat"], i["start_location"]["lng"])
        coordinates.append(start)

        coordinates.append(end_location)

    encoded_polyline = polyline.encode(coordinates)
    static_map_url = "https://maps.googleapis.com/maps/api/staticmap?size=400x400" + \
                     "&key=AIzaSyCDXE6q_zHm19AprJL4CvHn-HkNbaFMDro&path=enc:{0}".format(encoded_polyline)

    return static_map_url
