import sys
import joblib
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ml.features import FEATURE_COLUMNS

from app.services.team_features import (
    build_team_features,
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

def predict_game(
    db,
    home_team,
    away_team,
    season=None,
):

    if not MODEL_FILE.exists() or MODEL_FILE.stat().st_size == 0:
        return {
            "winner": None,
            "home_probability": None,
            "away_probability": None,
            "error": "Model not trained yet",
        }

    try:
        model = joblib.load(MODEL_FILE)
    except (EOFError, OSError, ValueError, AttributeError, ImportError):
        return {
            "winner": None,
            "home_probability": None,
            "away_probability": None,
            "error": "Model not trained or model file is invalid",
        }

    home = build_team_features(
        db,
        home_team,
        season=season,
    )

    away = build_team_features(
        db,
        away_team,
        season=season,
    )

    X = pd.DataFrame(
        [{
            "home_win_pct":
                home["win_pct"] / 100,

            "away_win_pct":
                away["win_pct"] / 100,

            "home_ppg":
                home["ppg"],

            "away_ppg":
                away["ppg"],

            "home_papg":
                home["papg"],

            "away_papg":
                away["papg"],
        }]
    )

    try:
        probability = float(model.predict_proba(X)[0][1])
    except (ValueError, AttributeError, TypeError) as exc:
        return {
            "winner": None,
            "home_probability": None,
            "away_probability": None,
            "error": f"Unable to generate prediction: {exc}",
        }

    home_probability = float(round(probability * 100, 1))

    away_probability = float(round((1 - probability) * 100, 1))

    winner = (
        home_team
        if home_probability >
        away_probability
        else away_team
    )

    win_pct_diff = round(
    home["win_pct"] -
    away["win_pct"],
    1,
)

    ppg_diff = round(
        home["ppg"] -
        away["ppg"],
        1,
    )

    papg_diff = round(
        away["papg"] -
        home["papg"],
        1,
    )

    point_diff_advantage = round(
        home["point_diff"] -
        away["point_diff"],
        1,
    )

    
    return {
        "winner": winner,
        "home_probability": home_probability,
        "away_probability": away_probability,
        "win_pct_diff": win_pct_diff,
        "ppg_diff": ppg_diff,
        "papg_diff": papg_diff,
        "point_diff_advantage": point_diff_advantage,

        "advantages": {

            "win_pct": {
                "leader":
                    home_team
                    if win_pct_diff > 0
                    else away_team,

                "value":
                    abs(win_pct_diff),
            },

            "ppg": {
                "leader":
                    home_team
                    if ppg_diff > 0
                    else away_team,

                "value":
                    abs(ppg_diff),
            },

            "papg": {
                "leader":
                    home_team
                    if papg_diff > 0
                    else away_team,

                "value":
                    abs(papg_diff),
            },

            "point_diff": {
                "leader":
                    home_team
                    if point_diff_advantage > 0
                    else away_team,

                "value":
                    abs(point_diff_advantage),
            },

        }
    }