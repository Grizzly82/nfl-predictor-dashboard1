from datetime import datetime


def transform_game(event, season=None, week=None):
    competition = event["competitions"][0]

    competitors = competition["competitors"]

    home = next(
        team
        for team in competitors
        if team["homeAway"] == "home"
    )

    away = next(
        team
        for team in competitors
        if team["homeAway"] == "away"
    )

    home_score = int(home["score"])
    away_score = int(away["score"])

    return {
        "external_game_id": event["id"],
        "game_date": datetime.fromisoformat(
            event["date"].replace("Z", "+00:00")
        ).date(),
        "season": season,
        "week": week,
        "home_team": home["team"]["abbreviation"],
        "away_team": away["team"]["abbreviation"],
        "home_score": home_score,
        "away_score": away_score,
        "home_win": home_score > away_score,
        "game_tie": home_score == away_score,
    }
