import sys
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sklearn.linear_model import (
    LogisticRegression,
)

from sklearn.model_selection import (
    train_test_split,
)

from sklearn.metrics import (
    accuracy_score,
)

from app.database.db import (
    SessionLocal,
)

from app.services.training_data import (
    build_training_dataframe,
)

def train_model():

    db = SessionLocal()

    try:

        df = build_training_dataframe(
            db
        )

        if df.empty or len(df) < 10:
            print("Not enough game history to train a model yet.")
            return

        X = df[
            [
                "home_win_pct",
                "away_win_pct",
                "home_ppg",
                "away_ppg",
                "home_papg",
                "away_papg",
            ]
        ]

        y = df["target"]

        (
            X_train,
            X_test,
            y_train,
            y_test,
        ) = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
        )

        model = LogisticRegression(max_iter=1000)

        model.fit(
            X_train,
            y_train,
        )

        predictions = model.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        print(
            f"Accuracy: {accuracy:.2%}"
        )

        joblib.dump(
            model,
            "app/ml/model.pkl",
        )

        print(
            "Model saved."
        )

    finally:

        db.close()


if __name__ == "__main__":
    train_model()