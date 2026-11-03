import pandas as pd

from app.database.models import Game
from app.utils.nfl import NFL_TEAM_ABBREVIATIONS


def total_games(db):
    """
    Total games in database.
    """
    return db.query(Game).count()


def total_teams(db):
    """
    Count unique teams.
    """

    games = db.query(Game).all()

    teams = set()

    for game in games:
        teams.add(game.home_team)
        teams.add(game.away_team)

    return len(teams)


def average_points_per_game(db):
    """
    Average combined points
    scored per game.
    """

    games = db.query(Game).all()

    if not games:
        return 0

    total_points = sum(
        game.home_score + game.away_score
        for game in games
    )

    return round(
        total_points / len(games),
        1,
    )


def home_field_advantage(db):
    """
    Home team win percentage.
    """

    games = db.query(Game).all()

    if not games:
        return 0

    non_ties = [
        game
        for game in games
        if not getattr(game, "game_tie", False)
        and game.home_score != game.away_score
    ]

    if not non_ties:
        return 0

    home_wins = sum(
        1
        for game in non_ties
        if game.home_win
    )

    percentage = (
        home_wins / len(non_ties)
    ) * 100

    return round(
        percentage,
        1,
    )


def top_scoring_teams(db):
    """
    Teams sorted by total points scored.
    """

    games = db.query(Game).all()

    team_points = {}

    for game in games:

        team_points[game.home_team] = (
            team_points.get(
                game.home_team,
                0
            )
            + game.home_score
        )

        team_points[game.away_team] = (
            team_points.get(
                game.away_team,
                0
            )
            + game.away_score
        )

    return sorted(
        team_points.items(),
        key=lambda x: x[1],
        reverse=True,
    )


def top_scoring_dataframe(db):
    """
    DataFrame for Plotly charts.
    """

    results = top_scoring_teams(db)[:10]

    return pd.DataFrame(
        results,
        columns=[
            "team",
            "points",
        ],
    )


def team_win_percentages(db):
    """
    Calculate win percentage
    of every team.
    """

    games = db.query(Game).all()

    stats = {}

    for game in games:

        home = game.home_team
        away = game.away_team

        if home not in stats:
            stats[home] = {
                "wins": 0,
                "ties": 0,
                "games": 0
            }

        if away not in stats:
            stats[away] = {
                "wins": 0,
                "ties": 0,
                "games": 0
            }

        stats[home]["games"] += 1
        stats[away]["games"] += 1

        is_tie = getattr(game, "game_tie", False)
        if is_tie is None:
            is_tie = game.home_score == game.away_score

        if is_tie:
            stats[home]["ties"] += 1
            stats[away]["ties"] += 1
        elif game.home_win:
            stats[home]["wins"] += 1
        else:
            stats[away]["wins"] += 1

    results = []

    for team, values in stats.items():

        pct = (
            (values["wins"] + values["ties"] * 0.5)
            / values["games"]
        ) * 100

        results.append(
            (
                team,
                round(
                    pct,
                    1,
                ),
            )
        )

    return sorted(
        results,
        key=lambda x: x[1],
        reverse=True,
    )


def team_win_percentage_dataframe(db):
    """
    DataFrame version of
    team win percentages.
    """

    results = team_win_percentages(db)

    return pd.DataFrame(
        results,
        columns=[
            "team",
            "win_percentage",
        ]
    )

from app.services.team_stats_service import (
    build_team_stats,
)


def get_team_summary(
    db,
    team_name,
):

    stats = build_team_stats(db)

    if team_name not in stats:
        return {
            "team": team_name,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "games_played": 0,
            "win_pct": 0.0,
            "ppg": 0.0,
            "papg": 0.0,
            "point_diff": 0.0,
        }

    team = stats[team_name]

    games = team["games"]

    if games == 0:
        ppg = 0.0
        papg = 0.0
        win_pct = 0.0
    else:
        ppg = team["points_for"] / games
        papg = team["points_against"] / games
        win_pct = round(
            (team["wins"] + team["ties"] * 0.5) / games * 100,
            1,
        )

    return {
        "team": team_name,
        "wins": team["wins"],
        "losses": team["losses"],
        "ties": team["ties"],
        "games_played": games,
        "win_pct": win_pct,
        "ppg": round(ppg, 1),
        "papg": round(papg, 1),
        "point_diff": round(
            ppg - papg,
            1,
        ),
    }

def get_all_teams(db):
    """
    Return all 32 NFL teams, including teams not playing in the
    current week's games.
    """

    # Use the canonical NFL list rather than database-only values so
    # bye weeks do not hide teams and legacy abbreviations do not add extras.
    return sorted(NFL_TEAM_ABBREVIATIONS)

def get_team_game_history(
    db,
    team_name,
):
    """
    Historical scoring trend.
    """

    games = db.query(Game).all()

    history = []

    for game in games:

        if game.home_team == team_name:

            history.append(
                {
                    "date": game.game_date,
                    "points": game.home_score,
                }
            )

        elif game.away_team == team_name:

            history.append(
                {
                    "date": game.game_date,
                    "points": game.away_score,
                }
            )

    df = pd.DataFrame(
        history
    )

    if not df.empty:
        df = df.sort_values(
            by="date"
        )

    return df

def compare_teams(
    db,
    team_a,
    team_b,
):
    """
    Compare two teams.
    """

    team_a_stats = get_team_summary(
        db,
        team_a,
    )

    team_b_stats = get_team_summary(
        db,
        team_b,
    )

    return {
        "team_a": team_a_stats,
        "team_b": team_b_stats,
    }