import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.startup import verify_environment

verify_environment()

from app.dashboard.callbacks import app, register_callbacks
from app.dashboard.layouts import layout

app.layout = layout
register_callbacks(app)

""" if __name__ == "__main__":
    app.run(debug=True)
 """

if __name__ == "__main__":
    app.run(
        debug=False
    )