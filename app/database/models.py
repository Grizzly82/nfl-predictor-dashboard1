from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
)

if __package__:
    from .db import Base
else:
    from db import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)

    game_date = Column(Date)

    home_team = Column(String)

    away_team = Column(String)

    home_score = Column(Integer)

    away_score = Column(Integer)

    home_win = Column(Boolean)