from fastapi import FastAPI

from app.api.analytics import router

app = FastAPI()

app.include_router(router)

## Analytics endpoints
@router.get("/home-field-advantage")
def get_home_field_advantage():

    db = SessionLocal()

    value = home_field_advantage(db)

    db.close()

    return {
        "home_win_percentage": value
    }

def ingest_games():
    """
    Pull games from ESPN
    and insert new records.
    """

    db = SessionLocal()

    inserted = 0

    try:

        data = get_scoreboard()

        events = data.get(
            "events",
            []
        )

        for event in events:

            game_data = transform_game(
                event
            )

            exists = game_exists(
                db,
                game_data[
                    "external_game_id"
                ],
            )

            if exists:
                continue

            insert_game(
                db,
                game_data,
            )

            inserted += 1

        print(
            f"{inserted} game(s) inserted."
        )

    finally:

        db.close()


        if __name__ == "__main__":
            ingest_games()