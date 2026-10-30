import requests
import pandas as pd

url = (
    "https://site.api.espn.com/apis/site/v2/"
    "sports/football/nfl/scoreboard"
)

response = requests.get(url)

data = response.json()

print(data.keys())