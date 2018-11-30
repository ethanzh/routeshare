import requests
import json
from bs4 import BeautifulSoup as bs

URL = "https://facilitiesservices.utexas.edu/buildings/UTM/0153"

data = requests.get(URL).text
soup = bs(data, features="html.parser")
for i in soup.find_all('h3'):
    print(i.text)

