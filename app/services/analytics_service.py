from sqlalchemy import func

from app.database.models import Game

#Top scoring teams based on total points scored in the season
def top_scoring_teams(db):

    games = db.query(Game).all()

    team_points = {}

    for game in games:

        team_points[game.home_team] = (
            team_points.get(game.home_team, 0)
            + game.home_score
        )

        team_points[game.away_team] = (
            team_points.get(game.away_team, 0)
            + game.away_score
        )

    return sorted(
        team_points.items(),
        key=lambda x: x[1],
        reverse=True
    )

#Team win percentages based on total wins and total games played
def team_win_percentages(db):

    games = db.query(Game).all()

    stats = {}

    for game in games:

        home = game.home_team
        away = game.away_team

        if home not in stats:
            stats[home] = {"wins": 0, "games": 0}

        if away not in stats:
            stats[away] = {"wins": 0, "games": 0}

        stats[home]["games"] += 1
        stats[away]["games"] += 1

        if game.home_win:
            stats[home]["wins"] += 1
        else:
            stats[away]["wins"] += 1

    results = []

    for team, values in stats.items():

        pct = values["wins"] / values["games"]

        results.append(
            (
                team,
                round(pct, 3)
            )
        )

    return sorted(
        results,
        key=lambda x: x[1],
        reverse=True
    )

#Home field advantage based on home team wins
def home_field_advantage(db):

    games = db.query(Game).all()

    total_games = len(games)

    home_wins = sum(
        1
        for game in games
        if game.home_win
    )

    pct = (
        home_wins
        / total_games
    ) * 100

    return round(pct, 2)

def get_team_summary(
    db,
    team_name
):

    games = db.query(Game).all()

    points_for = 0
    points_against = 0
    games_played = 0

    for game in games:

        if game.home_team == team_name:

            points_for += game.home_score

            points_against += game.away_score

            games_played += 1

        elif game.away_team == team_name:

            points_for += game.away_score

            points_against += game.home_score

            games_played += 1

    return {
        "team": team_name,
        "ppg": round(
            points_for / games_played,
            2
        ),
        "papg": round(
            points_against / games_played,
            2
        ),
    }