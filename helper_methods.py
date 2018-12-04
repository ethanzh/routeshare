import polyline
import pandas as pd
import requests

building_df = pd.read_csv("building_data.csv")


def two_lines(building_1, building_2, building_3, building_4):
    polyline_1 = get_polyline(building_1, building_2)
    polyline_2 = get_polyline(building_3, building_4)

    return "https://maps.googleapis.com/maps/api/staticmap?size=800x400" + \
           "&key=AIzaSyCDXE6q_zHm19AprJL4CvHn-HkNbaFMDro" + \
           "&path=color:red|enc:{0}&path=color:blue|enc:{1}".format(polyline_1, polyline_2)


def get_polyline(building_1, building_2):
    # Get building addresses
    class_1_address = building_df.loc[building_df['code'] == building_1]["address"].values[0]
    class_2_address = building_df.loc[building_df['code'] == building_2]["address"].values[0]

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

    return encoded_polyline
