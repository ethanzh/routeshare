import polyline
import pandas as pd
import requests

building_df = pd.read_csv("building_data.csv")


class Vertex:
    def __init__(self, lat, lng, slope):
        self.lat = lat
        self.lng = lng
        self.slope = slope

    def __str__(self):
        return "({0},{1}), m={2}".format(self.lat, self.lng, self.slope)

    def __eq__(self, other):
        # This is a temporary workaround, we want this to take
        # lat and lng into account also
        return abs(self.slope - other.slope) < 0.4


def map_url_from_polyline(encoded_polyline):
    return "https://maps.googleapis.com/maps/api/staticmap?size=800x400" + \
           "&key=AIzaSyCDXE6q_zHm19AprJL4CvHn-HkNbaFMDro" + \
           "&path=color:red|enc:{0}".format(encoded_polyline)


def two_lines(building_1, building_2, building_3, building_4):
    polyline_1 = get_polyline(building_1, building_2)
    polyline_2 = get_polyline(building_3, building_4)

    get_overlap(building_1, building_2, building_3, building_4)

    return "https://maps.googleapis.com/maps/api/staticmap?size=800x400" + \
           "&key=AIzaSyCDXE6q_zHm19AprJL4CvHn-HkNbaFMDro" + \
           "&path=color:red|enc:{0}&path=color:blue|enc:{1}".format(polyline_1, polyline_2)


def get_overlap(building_1, building_2, building_3, building_4):
    line_1 = get_coordinates(building_1, building_2)
    line_2 = get_coordinates(building_3, building_4)

    line_1_vertices = []
    line_2_vertices = []

    for i in range(len(line_1) - 1):
        current_slope = get_slope(line_1[i], line_1[i + 1])
        line_1_vertices.append(Vertex(line_1[i][0], line_1[i][1], current_slope))
    for i in range(len(line_2) - 1):
        current_slope = get_slope(line_2[i], line_2[i + 1])
        line_2_vertices.append(Vertex(line_2[i][0], line_2[i][1], current_slope))

    shared_vertices = []

    for i in range(0, len(line_1_vertices) - 1):
        if line_1_vertices[i] in line_2_vertices:
            shared_vertices.append(line_1_vertices[i])
            shared_vertices.append(line_1_vertices[i + 1])

    return get_map_from_coordinates(shared_vertices)


def get_map_from_coordinates(vertices):
    coordinates = [(x.lat, x.lng) for x in vertices]
    for i in coordinates:
        print(i)
    if len(coordinates) > 0:
        encoded_polyline = polyline.encode(coordinates)
    else:
        encoded_polyline = ""
    return map_url_from_polyline(encoded_polyline)


def get_slope(point_1, point_2):
    return (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])


def get_coordinates(building_1, building_2):
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

    return coordinates


def get_polyline(building_1, building_2):

    coordinates = get_coordinates(building_1, building_2)

    # Encode polyline, create URL
    encoded_polyline = polyline.encode(coordinates)

    return encoded_polyline
