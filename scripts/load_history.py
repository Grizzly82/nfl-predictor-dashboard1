import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.historical_loader import (
    load_season,
)

for year in [

    2021,
    2022,
    2023,
    2024,
    2025,
    2026,

]:

    load_season(
        year
    )