import sys
from pathlib import Path

# Allow this file to be run directly as well as through `python -m app.services...`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database.db import SessionLocal
from app.database.game_repository import game_exists, insert_game

try:
    from .espn_service import get_scoreboard
    from .game_transformer import transform_game
except ImportError:
    from espn_service import get_scoreboard
    from game_transformer import transform_game


def ingest_games():

    db = SessionLocal()

    data = get_scoreboard()

    inserted = 0

    for event in data["events"]:

        game = transform_game(event)

        if not game_exists(
            db,
            game["external_game_id"]
        ):
            insert_game(db, game)
            inserted += 1

    db.close()

    print(f"{inserted} games inserted")


if __name__ == "__main__":
    ingest_games()
