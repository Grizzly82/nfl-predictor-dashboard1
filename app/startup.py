from pathlib import Path

from app.config import settings


def verify_environment():

    print(
        "Checking application startup..."
    )

    if not settings.DATABASE_URL:
        raise ValueError(
            "DATABASE_URL missing"
        )

    model = (
        Path(
            settings.MODEL_PATH
        )
    )

    print("✓ DATABASE_URL found")

    if model.exists():

        print(
            "✓ Model file found"
        )

    else:

        print(
            "⚠ Model file missing"
        )