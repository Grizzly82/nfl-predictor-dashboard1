import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .db import Base, engine
    from .models import Game
except ImportError:
    from db import Base, engine
    from models import Game

Base.metadata.create_all(bind=engine)

with engine.begin() as connection:
    connection.exec_driver_sql(
        "ALTER TABLE games ADD COLUMN IF NOT EXISTS external_game_id VARCHAR"
    )
    connection.exec_driver_sql(
        "ALTER TABLE games ADD COLUMN IF NOT EXISTS season INTEGER"
    )
    connection.exec_driver_sql(
        "ALTER TABLE games ADD COLUMN IF NOT EXISTS week INTEGER"
    )
    connection.exec_driver_sql(
        "ALTER TABLE games ADD COLUMN IF NOT EXISTS game_tie BOOLEAN DEFAULT FALSE NOT NULL"
    )
    connection.exec_driver_sql(
        "UPDATE games SET game_tie = TRUE WHERE home_score = away_score AND home_score != 0 AND game_tie IS FALSE"
    )
    connection.exec_driver_sql(
        "UPDATE games SET game_tie = FALSE WHERE home_score = 0 AND away_score = 0"
    )
    connection.exec_driver_sql(
        "DELETE FROM games WHERE home_score = 0 AND away_score = 0"
    )

print("Tables created!")