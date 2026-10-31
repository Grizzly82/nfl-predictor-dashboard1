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