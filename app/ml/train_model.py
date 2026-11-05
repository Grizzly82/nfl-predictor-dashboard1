import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

from app.ml.features import FEATURE_COLUMNS

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

        X = df[FEATURE_COLUMNS]

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
            stratify=y,
        )

        print("\n===== EVALUATION =====")

        print(
            f"Total Rows: {len(df)}"
        )

        print(
            f"Train Rows: {len(X_train)}"
        )

        print(
            f"Test Rows: {len(X_test)}"
        )

        print(
            f"Home Wins: {y.sum()}"
        )

        print(
            f"Away Wins: {len(y) - y.sum()}"
        )

        print("======================\n")

        model = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=1000
                ),
            ),
        ]
    )

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

        import json

        metrics = {
         "accuracy": float(accuracy)
        }

        with open(
            "app/ml/metrics.json",
            "w"
        ) as f:

            json.dump(
                metrics,
                f,
                indent=4,
            )

        print("\n===== TRAINING DIAGNOSTICS =====")

        print(
            f"Training Rows: {len(df)}"
        )

        print(
            f"Training Set Size: {len(X_train)}"
        )

        print(
            f"Test Set Size: {len(X_test)}"
        )

        print(
            f"Unique Teams: {df.shape[0]}"
        )

        print(
            f"Accuracy: {accuracy:.2%}"
        )

        print("===============================\n")

        print(
            f"Accuracy: {accuracy:.2%}"
        )
        print(
            f"Training Rows: {len(df)}"
        )

        print(
            f"Training Set: {len(X_train)}"
        )

        print(
            f"Test Set: {len(X_test)}"
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