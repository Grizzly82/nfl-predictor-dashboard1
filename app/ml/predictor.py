import joblib
from pathlib import Path


from app.services.team_features import (
    build_team_features,
)

MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"


def predict_game(
    db,
    home_team,
    away_team,
):

    if not MODEL_PATH.exists() or MODEL_PATH.stat().st_size == 0:
        return {
            "winner": None,
            "home_probability": None,
            "away_probability": None,
            "error": "Model not trained yet",
        }

    try:
        model = joblib.load(MODEL_PATH)
    except (EOFError, OSError, ValueError):
        return {
            "winner": None,
            "home_probability": None,
            "away_probability": None,
            "error": "Model not trained or model file is invalid",
        }

    home = build_team_features(
        db,
        home_team,
    )

    away = build_team_features(
        db,
        away_team,
    )

    X = [[
        home["win_pct"] / 100,
        away["win_pct"] / 100,
        home["ppg"],
        away["ppg"],
        home["papg"],
        away["papg"],
    ]]

    probability = (
        model.predict_proba(X)[0][1]
    )

    home_probability = round(
        probability * 100,
        1,
    )

    away_probability = round(
        (1 - probability) * 100,
        1,
    )

    winner = (
        home_team
        if home_probability >
        away_probability
        else away_team
    )

    return {
        "winner": winner,
        "home_probability":
            home_probability,
        "away_probability":
            away_probability,
    }