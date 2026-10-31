from app.database.models import Game


def game_exists(db, external_game_id):
    return (
        db.query(Game)
        .filter(
            Game.external_game_id == external_game_id
        )
        .first()
        is not None
    )


def insert_game(db, game_data):

    game = Game(**game_data)

    db.add(game)

    db.commit()

    return game