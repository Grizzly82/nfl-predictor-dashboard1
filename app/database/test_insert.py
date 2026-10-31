from datetime import date

from db import SessionLocal
from models import Game

db = SessionLocal()

game = Game(
    game_date=date.today(),
    home_team="KC",
    away_team="BUF",
    home_score=31,
    away_score=24,
    home_win=True,
)

db.add(game)

db.commit()

db.close()

print("Game inserted!")