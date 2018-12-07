import polyline
import pandas as pd
import requests

building_df = pd.read_csv("building_data.csv")


class Vertex:
    def __init__(self, lat, lng, slope, next_lat, next_lng):
        self.lat = lat
        self.lng = lng
        self.slope = slope
        self.next_lat = next_lat
        self.next_lng = next_lng

    def __str__(self):
        return "({0},{1}), m={2}".format(self.lat, self.lng, self.slope)

    def __eq__(self, other):
        # This is a temporary workaround, we want this to take
        # lat and lng into account also
        # Return true if slopes are within 10% of each other
        return abs((self.slope - other.slope) / other.slope) * 100 < 10


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
        line_1_vertices.append(Vertex(line_1[i][0], line_1[i][1], current_slope, line_1[i + 1][0], line_1[i + 1][1]))
    for i in range(len(line_2) - 1):
        current_slope = get_slope(line_2[i], line_2[i + 1])
        line_2_vertices.append(Vertex(line_2[i][0], line_2[i][1], current_slope, line_2[i + 1][0], line_2[i + 1][1]))

    shared_vertices = []

    """
    for i in range(0, len(line_1_vertices) - 1):
        if i in line_2_vertices:
            shared_vertices.append(line_1_vertices[i])
            shared_vertices.append(line_1_vertices[i + 1])
            
            for j in range(0, len(line_2_vertices)):
                if line_1_vertices[i] == line_2_vertices[j]:
                    shared_vertices.append(line_1_vertices[i])
                    shared_vertices.append(line_1_vertices[i + 1])
                    #print(line_1_vertices[i].slope)
            #if line_1_vertices[i] in line_2_vertices:
            
    """


    # We want behavior to change as soon as we find a match
    # It shouldn't matter where we start from, because we only care about overlap
    # Go to first 'equal' spot

    # made index_1 relate to the larger list
    if len(line_1_vertices) > len(line_2_vertices):
        traverse = line_1_vertices
        other = line_2_vertices
    else:
        traverse = line_2_vertices
        other = line_2_vertices

    i1 = -1
    j2 = -1

    for i in range(0, len(traverse)):
        for j in range(0, len(other)):
            if i == j:
                i1 = i
                j2 = j
                break

    shared_vertices.append(traverse[i1])

    filtered_traverse = traverse[i1 + 1:]
    filtered_other = traverse[j2 + 1:]

    if len(filtered_traverse) > len(filtered_other):
        even_more_filtered = filtered_traverse
        even_more_filtered_other = filtered_other
    else:
        even_more_filtered = filtered_other
        even_more_filtered_other = filtered_traverse

    # both lists start at 0

    # continue from known 'same' point
    for i in range(0, len(even_more_filtered_other)):
        if even_more_filtered[i] == even_more_filtered_other[i]:
            shared_vertices.append(even_more_filtered[i])
        else:
            break

    print(shared_vertices)

    return get_map_from_coordinates(shared_vertices)


def get_map_from_coordinates(vertices):
    coordinates = [(x.lat, x.lng) for x in vertices]

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

    print(url)

    # Get only the data needed from API resopnse
    data = requests.get(url).json()["routes"][0]["legs"][0]

    print(data)
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
