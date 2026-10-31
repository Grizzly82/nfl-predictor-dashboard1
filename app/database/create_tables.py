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

print("Tables created!")