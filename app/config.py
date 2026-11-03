import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )

    MODEL_PATH = (
        "app/ml/model.pkl"
    )

    RANDOM_FOREST_PATH = (
        "app/ml/random_forest.pkl"
    )


settings = Settings()