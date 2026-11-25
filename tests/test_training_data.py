import os
import sys
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite://")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.db import Base
from app.database.models import Game
from app.services.training_data import build_training_dataframe


def _insert_games(db, season, first_game_number, scores):
    for game_number, (home_score, away_score) in enumerate(
        scores, start=first_game_number
    ):
        db.add(
            Game(
                external_game_id=f"{season}-{game_number}",
                game_date=date(season, 9, game_number),
                season=season,
                week=game_number,
                home_team="AAA",
                away_team="BBB",
                home_score=home_score,
                away_score=away_score,
                home_win=home_score > away_score,
                game_tie=home_score == away_score,
            )
        )
    db.commit()


def test_training_dataframe_uses_only_latest_season_games():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as db:
            _insert_games(db, 2024, 1, [(100, 0)] * 4)
            _insert_games(db, 2025, 1, [(20, 10), (30, 10), (40, 10), (50, 10)])

            training_data = build_training_dataframe(db)

        assert len(training_data) == 4
        assert training_data.iloc[0]["home_ppg"] == 100
        assert training_data.iloc[-1]["home_ppg"] == 70
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_training_dataframe_is_empty_without_seasoned_games():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as db:
            assert build_training_dataframe(db).empty
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()
