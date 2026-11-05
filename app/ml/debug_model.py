import joblib
from pathlib import Path

model = joblib.load(
    Path(__file__).parent / "model.pkl"
)

estimator = model.named_steps["model"]

features = [

    "home_win_pct",
    "away_win_pct",

    "home_ppg",
    "away_ppg",

    "home_papg",
    "away_papg",

    "home_point_diff",
    "away_point_diff",
]

print("\n===== MODEL WEIGHTS =====\n")

for feature, coef in zip(
    features,
    estimator.coef_[0],
):

    print(
        f"{feature:<25} {coef:.4f}"
    )