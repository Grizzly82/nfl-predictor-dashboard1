if __package__:
    from .db import Base, engine
    from .models import Game
else:
    from db import Base, engine
    from models import Game

Base.metadata.create_all(bind=engine)

print("Tables created!")