import requests

BASE_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
)


def get_scoreboard(season=None, week=None):
    params = {}
    if season is not None:
        params["dates"] = season
    if week is not None:
        params["week"] = week
        params["seasontype"] = 2

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    return response.json()