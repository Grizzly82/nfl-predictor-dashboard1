from sqlalchemy import Index
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
)

try:
    from .db import Base
except ImportError:
    from db import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)

    #added external_game_id column to store the unique identifier for each game
    external_game_id = Column(String, unique=True)

    game_date = Column(Date)

    season = Column(Integer)

    week = Column(Integer)

    home_team = Column(
    String,
    index=True,
    )

    away_team = Column(
        String,
        index=True,
    )


    game_date = Column(
        Date,
        index=True,
    )

    season = Column(
    Integer,
    index=True,
)
    home_score = Column(Integer)

    away_score = Column(Integer)

    home_win = Column(Boolean)
    game_tie = Column(Boolean, default=False, nullable=False)

    __table_args__ = (

    Index(
        "idx_season_week",
        "season",
        "week",
    ),

)