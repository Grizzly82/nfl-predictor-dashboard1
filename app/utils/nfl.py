from datetime import datetime, timedelta

import requests


NFL_TEAM_ABBREVIATIONS = (
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LV", "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS",
)


def get_current_nfl_season():
    """
    NFL season starts in September.
    Jan-Aug belong to the previous season.
    """

    today = datetime.now()

    if today.month >= 9:
        return today.year

    return today.year - 1


def get_current_nfl_week():
    """
    Get the current NFL week from ESPN, with a date-based fallback.
    """

    try:
        response = requests.get(
            "https://site.api.espn.com/apis/site/v2/"
            "sports/football/nfl/scoreboard",
            timeout=5,
        )
        response.raise_for_status()
        week = response.json().get("week", {}).get("number")
        if week:
            return int(week)
    except (requests.RequestException, ValueError, TypeError):
        pass

    today = datetime.now().date()
    season = get_current_nfl_season()
    season_start = datetime(season, 9, 1).date()

    days_until_thursday = (3 - season_start.weekday()) % 7
    first_week = season_start + timedelta(days=days_until_thursday)

    if today < first_week:
        return 1

    return min(((today - first_week).days // 7) + 1, 18)