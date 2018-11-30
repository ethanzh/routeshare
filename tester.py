import requests
import json

URL = "https://maps.googleapis.com/maps/api/directions/json?origin=2317 Speedway, Austin TX, 78712&destination=110 Inner Campus Dr, Austin TX, 78712&key=AIzaSyCDXE6q_zHm19AprJL4CvHn-HkNbaFMDro&mode=walking"
data = requests.get(URL).json()

overview_polyline = data["routes"][0]["overview_polyline"]["points"]
end_location = data["routes"][0]["legs"][0]["end_location"]
end_location = (end_location["lat"], end_location["lng"])
data = data["routes"][0]["legs"][0]["steps"] 
locs = []
for i in data:
    start = (i["start_location"]["lat"], i["start_location"]["lng"])
    locs.append(start)
    print(str(start[0]) + ", " + str(start[1]) + ", " + "test" + ", " + "red")

locs.append(end_location)

# we now have a list of all coordinates, which are hopefully shared on different google maps routes
# we should round at some point
