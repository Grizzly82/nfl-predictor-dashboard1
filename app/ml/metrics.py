import joblib
from pathlib import Path

import pandas as pd
from pathlib import Path

import joblib

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    roc_curve,
    auc,
)

from sklearn.model_selection import (
    train_test_split,
)

from app.database.db import (
    SessionLocal,
)

from app.services.training_data import (
    build_training_dataframe,
)


#MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
)

MODEL_FILE = (
    BASE_DIR / "model.pkl"
)

model = joblib.load(
    MODEL_FILE
)

def _empty_model_metrics():
    return {
        "accuracy": 0.0,
        "confusion_matrix": [[0, 0], [0, 0]],
        "fpr": [],
        "tpr": [],
        "roc_auc": 0.0,
    }


def _load_model():
    if not MODEL_FILE.exists() or MODEL_FILE.stat().st_size == 0:
        return None

    try:
        return joblib.load(MODEL_FILE)
    except (EOFError, OSError, ValueError):
        return None


def evaluate_model():
    model = _load_model()
    if model is None:
        return _empty_model_metrics()

    db = SessionLocal()

    try:
        df = build_training_dataframe(db)

        if df.empty or len(df) < 5:
            return _empty_model_metrics()

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

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
        )

        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, predictions)
        cm = confusion_matrix(y_test, predictions)
        fpr, tpr, _ = roc_curve(y_test, probabilities)
        roc_auc = auc(fpr, tpr)

        return {
            "accuracy": accuracy,
            "confusion_matrix": cm,
            "fpr": fpr,
            "tpr": tpr,
            "roc_auc": roc_auc,
        }
    finally:
        db.close()


def get_feature_importance():
    model = _load_model()
    if model is None or not hasattr(model, "coef_"):
        return pd.DataFrame({"feature": [], "importance": []})

    features = [
        "home_win_pct",
        "away_win_pct",
        "home_ppg",
        "away_ppg",
        "home_papg",
        "away_papg",
    ]

    coeffs = model.coef_[0]
    results = pd.DataFrame(
        {
            "feature": features,
            "importance": abs(coeffs),
        }
    )

    return results.sort_values(by="importance", ascending=False)