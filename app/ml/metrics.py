import sys
import joblib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import json

from app.ml.features import FEATURE_COLUMNS

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
    except (EOFError, OSError, ValueError, AttributeError, ImportError):
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

        X = df[FEATURE_COLUMNS]
        y = df["target"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        cm = confusion_matrix(y_test, predictions, labels=[0, 1])

        if len(set(y_test)) < 2:
            fpr, tpr, roc_auc = [], [], 0.0
        else:
            probabilities = model.predict_proba(X_test)[:, 1]
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
    if model is None:
        return pd.DataFrame({"feature": [], "importance": []})

    if hasattr(model, "named_steps"):
        estimator = model.named_steps.get("model")
    else:
        estimator = model

    if estimator is None or not hasattr(estimator, "coef_"):
        return pd.DataFrame({"feature": [], "importance": []})

    features = getattr(model, "feature_names_in_", None)
    if features is None:
        features = getattr(estimator, "feature_names_in_", None)
    if features is None:
        features = FEATURE_COLUMNS

    coeffs = estimator.coef_[0]
    if len(features) != len(coeffs):
        return pd.DataFrame({"feature": [], "importance": []})

    results = pd.DataFrame(
        {
            "feature": list(features),
            "importance": abs(coeffs),
        }
    )

    return results.sort_values(by="importance", ascending=False)