import requests
from datetime import datetime

from app.database.db import SessionLocal
from app.database.models import Game
from app.services.game_transformer import transform_game


def load_week(season: int, week: int):
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    params = {"dates": season, "week": week, "seasontype": 2}

    print(f"\nLoading NFL {season} Week {week}")
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    events = response.json().get("events", [])

    if not events:
        print(f"No games found for {season} Week {week}")
        return 0

    db = SessionLocal()
    inserted = 0
    repaired = 0
    skipped = 0

    try:
        for event in events:
            competition = event["competitions"][0]
            status = competition.get("status", {}).get("type", {})
            if not status.get("completed"):
                continue

            competitors = competition["competitors"]
            home = next(team for team in competitors if team["homeAway"] == "home")
            away = next(team for team in competitors if team["homeAway"] == "away")
            if int(home["score"]) == 0 and int(away["score"]) == 0:
                continue

            external_game_id = event["id"]
            existing = db.query(Game).filter(
                Game.external_game_id == external_game_id
            ).first()
            if existing:
                if existing.season is None or existing.week is None:
                    game_data = transform_game(event, season=season, week=week)
                    for field, value in game_data.items():
                        setattr(existing, field, value)
                    repaired += 1
                    continue

                skipped += 1
                continue

            game_data = transform_game(event, season=season, week=week)
            db.add(Game(**game_data))
            inserted += 1

        db.commit()
        print(
            f"Inserted {inserted} games | Repaired {repaired} incomplete "
            f"records | Skipped {skipped} duplicates"
        )
        return inserted
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def load_season(season: int):
    total = 0
    for week in range(1, 19):
        total += load_week(season, week)
    print(f"{season}: {total} games inserted")
    return total
