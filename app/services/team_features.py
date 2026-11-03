from app.database.models import Game

from app.services.analytics_service import (
    get_team_summary,
    get_all_teams,
    get_team_game_history,
    compare_teams,
)



def get_recent_form(
    db,
    team_name,
    last_n=5,
):
    """
    Number of wins in the last N games.
    """

    games = db.query(Game).all()

    team_games = []

    for game in games:

        if (
            game.home_team == team_name
            or game.away_team == team_name
        ):
            team_games.append(game)

    team_games.sort(
        key=lambda x: x.game_date,
        reverse=True,
    )

    recent_games = team_games[:last_n]

    wins = 0

    for game in recent_games:

        if (
            game.home_team == team_name
            and game.home_win
        ):
            wins += 1

        elif (
            game.away_team == team_name
            and not game.home_win
        ):
            wins += 1

    return wins

def get_win_streak(
    db,
    team_name,
):
    """
    Current win streak.
    """

    games = db.query(Game).all()

    team_games = []

    for game in games:

        if (
            game.home_team == team_name
            or game.away_team == team_name
        ):
            team_games.append(game)

    team_games.sort(
        key=lambda x: x.game_date,
        reverse=True,
    )

    streak = 0

    for game in team_games:

        won = False

        if (
            game.home_team == team_name
            and game.home_win
        ):
            won = True

        elif (
            game.away_team == team_name
            and not game.home_win
        ):
            won = True

        if won:
            streak += 1
        else:
            break

    return streak


def build_team_features(
    db,
    team_name,
):
    """
    Build reusable team features.
    """

    summary = get_team_summary(
        db,
        team_name,
    )

    if summary is None:
        return None

    recent_form = get_recent_form(
        db,
        team_name,
    )

    win_streak = get_win_streak(
        db,
        team_name,
    )

    return {
        "team": team_name,
        "wins": summary["wins"],
        "losses": summary["losses"],
        "games_played": summary["games_played"],
        "win_pct": summary["win_pct"],
        "ppg": summary["ppg"],
        "papg": summary["papg"],
        "point_diff": summary["point_diff"],
        "recent_form": recent_form,
        "win_streak": win_streak,
    }