from collections import defaultdict

from app.database.models import Game


def build_team_stats(db, season=None):

    query = db.query(Game)
    if season is not None:
        query = query.filter(Game.season == season)
    games = query.all()

    stats = defaultdict(
        lambda: {
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "games": 0,
            "points_for": 0,
            "points_against": 0,
        }
    )

    for game in games:

        home = game.home_team
        away = game.away_team

        stats[home]["games"] += 1
        stats[away]["games"] += 1

        stats[home]["points_for"] += (
            game.home_score
        )

        stats[home]["points_against"] += (
            game.away_score
        )

        stats[away]["points_for"] += (
            game.away_score
        )

        stats[away]["points_against"] += (
            game.home_score
        )

        is_tie = getattr(game, "game_tie", False)
        if is_tie is None:
            is_tie = game.home_score == game.away_score

        if is_tie:
            stats[home]["ties"] += 1
            stats[away]["ties"] += 1
        elif game.home_win:
            stats[home]["wins"] += 1
            stats[away]["losses"] += 1
        else:
            stats[away]["wins"] += 1
            stats[home]["losses"] += 1

    return stats
