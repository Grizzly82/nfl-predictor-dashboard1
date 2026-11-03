import pandas as pd

from app.database.models import Game


def build_training_dataframe(db):

    games = (
        db.query(Game)
        .order_by(Game.game_date)
        .all()
    )

    records = []

    team_stats = {}

    for game in games:

        home_team = game.home_team
        away_team = game.away_team

        if home_team not in team_stats:
            team_stats[home_team] = {
                "games": 0,
                "wins": 0,
                "points_for": 0,
                "points_against": 0,
            }

        if away_team not in team_stats:
            team_stats[away_team] = {
                "games": 0,
                "wins": 0,
                "points_for": 0,
                "points_against": 0,
            }

        home = team_stats[home_team]
        away = team_stats[away_team]

        # Skip teams with no history yet

        if (
            home["games"] >= 3
            and away["games"] >= 3
        ):

            home_win_pct = (
                home["wins"] /
                home["games"]
            )

            away_win_pct = (
                away["wins"] /
                away["games"]
            )

            home_ppg = (
                home["points_for"] /
                home["games"]
            )

            away_ppg = (
                away["points_for"] /
                away["games"]
            )

            home_papg = (
                home["points_against"] /
                home["games"]
            )

            away_papg = (
                away["points_against"] /
                away["games"]
            )

            records.append(
                {
                    "home_win_pct": home_win_pct,
                    "away_win_pct": away_win_pct,
                    "home_ppg": home_ppg,
                    "away_ppg": away_ppg,
                    "home_papg": home_papg,
                    "away_papg": away_papg,
                    "target": int(
                        game.home_win
                    ),
                }
            )

        home["games"] += 1
        away["games"] += 1

        home["points_for"] += game.home_score
        home["points_against"] += game.away_score

        away["points_for"] += game.away_score
        away["points_against"] += game.home_score

        if game.home_win:
            home["wins"] += 1
        else:
            away["wins"] += 1

    return pd.DataFrame(records)