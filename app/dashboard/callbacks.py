from turtle import pd

import plotly.express as px

from dash import Dash, Input, Output, html
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.FONT_AWESOME,
    ],
)
server = app.server

from app.database.db import (
    SessionLocal,
)

from app.ml.metrics import (
    evaluate_model,
    get_feature_importance,
)


from app.services.analytics_service import (
    total_games,
    total_teams,
    average_points_per_game,
    home_field_advantage,
    top_scoring_dataframe,
    team_win_percentage_dataframe,
    get_all_teams,
    get_team_summary,
    get_team_game_history,
    compare_teams,
)

from app.ml.predictor import (
    predict_game,
)


def register_callbacks(app):

    @app.callback(
        [
            Output("games-card", "children"),
            Output("teams-card", "children"),
            Output("ppg-card", "children"),
            Output("home-card", "children"),
        ],
        Input("games-card", "id"),
    )
    def update_metrics(_):

        db = SessionLocal()

        try:

            return (
                total_games(db),
                total_teams(db),
                average_points_per_game(db),
                f"{home_field_advantage(db)}%",
            )

        finally:
            db.close()

    @app.callback(
        Output(
            "top-scoring-chart",
            "figure",
        ),
        Input(
            "top-scoring-chart",
            "id",
        ),
    )
    def update_top_scoring_chart(_):

        db = SessionLocal()

        try:

            df = top_scoring_dataframe(
                db
            )

            fig = px.bar(
                df,
                x="team",
                y="points",
                title="Top Scoring Teams",
            )

            return fig

        finally:
            db.close()

    @app.callback(
        Output(
            "win-percentage-chart",
            "figure",
        ),
        Input(
            "win-percentage-chart",
            "id",
        ),
    )
    def update_win_chart(_):

        db = SessionLocal()

        try:

            df = (
                team_win_percentage_dataframe(
                    db
                )
            )

            fig = px.bar(
                df.head(10),
                x="team",
                y="win_percentage",
                title="Top Win Percentages",
            )

            return fig

        finally:
            db.close()

    @app.callback(
        [
            Output(
                "team-dropdown",
                "options",
            ),
            Output(
                "team-a-dropdown",
                "options",
            ),
            Output(
                "team-b-dropdown",
                "options",
            ),
        ],
        Input(
            "team-dropdown",
            "id",
        ),
    )
    def populate_dropdowns(_):

        db = SessionLocal()

        try:

            teams = get_all_teams(
                db
            )

            options = [
                {
                    "label": team,
                    "value": team,
                }
                for team in teams
            ]

            return (
                options,
                options,
                options,
            )

        finally:
            db.close()

    @app.callback(
        [
            Output(
                "team-wins",
                "children",
            ),
            Output(
                "team-losses",
                "children",
            ),
            Output(
                "team-ppg",
                "children",
            ),
            Output(
                "team-papg",
                "children",
            ),
            Output(
                "team-win-pct",
                "children",
            ),
        ],
        Input(
            "team-dropdown",
            "value",
        ),
    )
    def update_team_cards(team):

        if not team:
            return "-", "-", "-", "-", "-"

        db = SessionLocal()

        try:

            summary = (
                get_team_summary(
                    db,
                    team,
                )
            )

            return (
                summary["wins"],
                summary["losses"],
                summary["ppg"],
                summary["papg"],
                summary["win_pct"],
            )

        finally:
            db.close()

    @app.callback(
        Output(
            "team-trend-chart",
            "figure",
        ),
        Input(
            "team-dropdown",
            "value",
        ),
    )
    def update_team_chart(team):

        fig = px.line()

        if not team:
            return fig

        db = SessionLocal()

        try:

            df = (
                get_team_game_history(
                    db,
                    team,
                )
            )

            if df.empty:
                return fig

            return px.line(
                df,
                x="date",
                y="points",
                markers=True,
                title=(
                    f"{team} Scoring Trend"
                ),
            )

        finally:
            db.close()

    @app.callback(
        Output(
            "comparison-table",
            "children",
        ),
        [
            Input(
                "team-a-dropdown",
                "value",
            ),
            Input(
                "team-b-dropdown",
                "value",
            ),
        ],
    )
    def update_comparison(
        team_a,
        team_b,
    ):

        if not team_a or not team_b:
            return "Select two teams"

        db = SessionLocal()

        try:

            comparison = (
                compare_teams(
                    db,
                    team_a,
                    team_b,
                )
            )

            a = comparison["team_a"]
            b = comparison["team_b"]

            return dbc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th(
                                    "Metric"
                                ),
                                html.Th(
                                    team_a
                                ),
                                html.Th(
                                    team_b
                                ),
                            ]
                        )
                    ),
                    html.Tbody(
                        [
                            html.Tr([
                                html.Td("Wins"),
                                html.Td(a["wins"]),
                                html.Td(b["wins"]),
                            ]),
                            html.Tr([
                                html.Td("Losses"),
                                html.Td(a["losses"]),
                                html.Td(b["losses"]),
                            ]),
                            html.Tr([
                                html.Td("PPG"),
                                html.Td(a["ppg"]),
                                html.Td(b["ppg"]),
                            ]),
                            html.Tr([
                                html.Td("PAPG"),
                                html.Td(a["papg"]),
                                html.Td(b["papg"]),
                            ]),
                            html.Tr([
                                html.Td("Point Diff"),
                                html.Td(
                                    a["point_diff"]
                                ),
                                html.Td(
                                    b["point_diff"]
                                ),
                            ]),
                        ]
                    )
                ],
                bordered=True,
                striped=True,
                hover=True,
            )

        finally:
            db.close()

    @app.callback(
        Output(
            "prediction-output",
            "children",
        ),
        [
            Input(
                "team-a-dropdown",
                "value",
            ),
            Input(
                "team-b-dropdown",
                "value",
            ),
        ],
    )
    def update_prediction(
        team_a,
        team_b,
    ):

        if not team_a or not team_b:
            return "Select two teams."

        db = SessionLocal()

        try:

            prediction = predict_game(
                db,
                team_a,
                team_b,
            )

            if prediction.get("error"):
                return prediction["error"]

            return (
                f"Winner: "
                f"{prediction['winner']} | "
                f"{team_a}: "
                f"{prediction['home_probability']}% | "
                f"{team_b}: "
                f"{prediction['away_probability']}%"
            )

        finally:
            db.close()


@app.callback(
    [
        Output("model-accuracy", "children"),
        Output("model-roc", "children"),
    ],
    Input("model-accuracy", "id"),
)
def update_model_metrics(_):
    metrics = evaluate_model()

    return (
        f"{metrics['accuracy']:.2%}",
        f"{metrics['roc_auc']:.3f}",
    )

@app.callback(
    Output(
        "confusion-matrix-chart",
        "figure"
    ),
    Input(
        "confusion-matrix-chart",
        "id"
    ),
)
def update_confusion_matrix(_):

    metrics = evaluate_model()

    cm = metrics[
        "confusion_matrix"
    ]

    fig = px.imshow(
        cm,
        text_auto=True,
        title="Confusion Matrix"
    )

    return fig

@app.callback(
    Output(
        "roc-chart",
        "figure"
    ),
    Input(
        "roc-chart",
        "id"
    ),
)
def update_roc_curve(_):

    metrics = evaluate_model()

    fig = px.line(
        x=metrics["fpr"],
        y=metrics["tpr"],
        title="ROC Curve",
    )

    return fig

@app.callback(
    Output(
        "feature-importance-chart",
        "figure"
    ),
    Input(
        "feature-importance-chart",
        "id"
    ),
)
def update_feature_importance(_):

    df = get_feature_importance()

    fig = px.bar(
        df,
        x="feature",
        y="importance",
        title="Feature Importance"
    )

    return fig