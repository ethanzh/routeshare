import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd

df = pd.DataFrame(columns=['code', 'name', 'address'])

BASE_URL = "https://facilitiesservices.utexas.edu"

# get the page as HTML
data = requests.get(BASE_URL + "/buildings").text
# create soup object
soup = bs(data, features="html.parser")

tables = soup.findAll("table")
# retrieve table where all building info is stored
#table = soup.find( "table", {"class":"buildinglist"})

# inner class to represent buildings
class Building():

    def __init__(self):
        self.name = None
        self.code = None
        self.url = None
        self.address = None

data_for_dataframe = {
    "code": [],
    "name": [],
    "address": []
}
building_objects = []
for table in tables:
    for row in table.findAll("tr"):
        current_building = Building()

        if len(row.findAll("td")) > 0:
            for td in row.findAll("td"):
                entry_text = td.renderContents().strip().decode('UTF-8')

                if entry_text[0] == "<":
                    split_list = entry_text.split('"') # makes it easy to get link
                    rel_link = split_list[1] # get /buildings/UTM/num#/
                    abbrev = split_list[2] # get form '>GDC</a>'
                    abbrev = abbrev[1:]
                    abbrev = abbrev[0:3]

                    current_building.url = rel_link
                    current_building.code = abbrev

                # get first character
                elif entry_text[0][0].isalpha():
                    building_name = entry_text
                    current_building.name = building_name

            current_url = BASE_URL + current_building.url
            current_html = requests.get(current_url).text
            current_soup = bs(current_html, features="html.parser")

            for i in current_soup.find_all('h3'):
                current_building.address = i.text.replace(',', '')
                data_for_dataframe["code"].append(current_building.code)
                data_for_dataframe["name"].append(current_building.name)
                data_for_dataframe["address"].append(current_building.address)
                print("done with", current_building.code, current_building.address)

df = pd.DataFrame(data=data_for_dataframe)
df.to_csv("building_data.csv", encoding='utf-8')
