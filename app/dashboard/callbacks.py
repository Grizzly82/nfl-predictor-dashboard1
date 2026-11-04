import pandas as pd
from app.database import db
import plotly.express as px
import plotly.graph_objects as go
from app.assets.team_assets import TEAM_INFO
from dash import Dash, Input, Output, html, dcc
import dash_bootstrap_components as dbc

""" app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.FONT_AWESOME,
    ],
)
server = app.server """
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY
    ]
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


@app.callback(
    Output("team-card", "style"),
    Input("team-dropdown", "value")
)
def update_team_theme(team):

    if not team:
        return {}

    return {
        "backgroundColor":
            TEAM_INFO[team]["primary"],
        "color": "white",
    }

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
    def update_league_metrics(_):
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

            fig = go.Figure(
                data=[go.Bar(
                    x=df["team"].tolist(),
                    y=df["points"].tolist(),
                )]
            )
            fig.update_layout(
                title="Top Scoring Teams",
                template="plotly_white",
                xaxis_title="Team",
                yaxis_title="Points",
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

            df = df.head(10)
            fig = go.Figure(
                data=[go.Bar(
                    x=df["team"].tolist(),
                    y=df["win_percentage"].tolist(),
                )]
            )
            fig.update_layout(
                title="Top Win Percentages",
                template="plotly_white",
                xaxis_title="Team",
                yaxis_title="Win Percentage",
                yaxis_range=[0, 100],
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
                "team-ties",
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
            Output(
                "team-point-diff",
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
            return "-", "-", "-", "-", "-", "-", "-"

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
                summary["ties"],
                summary["ppg"],
                summary["papg"],
                f"{summary['win_pct']}%",
                summary["point_diff"],
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
                                html.Td("Ties"),
                                html.Td(a["ties"]),
                                html.Td(b["ties"]),
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

            home_gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=prediction["home_probability"],
                    title={
                        "text":
                            f"{team_a} Win Probability"
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100]
                        },
                        "bar": {
                            "color": TEAM_INFO[team_a]["primary"]
                         }
                    }
                )
            )

            away_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=prediction["away_probability"],
                title={
                    "text":
                        f"{team_b} Win Probability"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": TEAM_INFO[team_b]["primary"]
                    },
                }
            )
        )

            winner = prediction["winner"]

            return dbc.Container(
                [
                    dbc.Alert(
                        f"🏆 Predicted Winner: {winner}",
                        color="success",
                        className="text-center",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=home_gauge,
                                    config={"displayModeBar": False},
                                ),
                                xs=12,
                                md=6,
                                className="text-center",
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    figure=away_gauge,
                                    config={"displayModeBar": False},
                                ),
                                xs=12,
                                md=6,
                                className="text-center",
                            ),
                        ],
                        className="align-items-center w-100 g-3",
                    ),
                ],
                fluid=True,
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

    if len(metrics["fpr"]) == 0 or len(metrics["tpr"]) == 0:
        return px.line(title="ROC Curve - Not Enough Data")

    roc_df = pd.DataFrame(
        {
            "False Positive Rate": metrics["fpr"],
            "True Positive Rate": metrics["tpr"],
        }
    )

    fig = px.line(
        roc_df,
        x="False Positive Rate",
        y="True Positive Rate",
        title="ROC Curve",
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_range=[0, 1],
        yaxis_range=[0, 1],
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

    fig = go.Figure(
        data=[go.Bar(
            x=df["feature"].tolist() if not df.empty else [],
            y=df["importance"].tolist() if not df.empty else [],
        )]
    )
    fig.update_layout(
        title="Feature Importance",
        template="plotly_white",
        xaxis_title="Feature",
        yaxis_title="Importance",
    )

    return fig

@app.callback(
    Output(
        "team-logo-container",
        "children"
    ),
    Input(
        "team-dropdown",
        "value"
    )
)
def update_team_logo(team):

    if not team:
        return ""

    return html.Div(
        [
            html.Img(
                src=TEAM_INFO[team]["logo"],
                style={"height": "120px"}
            ),
            html.H3(
                TEAM_INFO[team]["name"],
                style={
                    "color": TEAM_INFO[team]["primary"],
                    "marginTop": "10px",
                }
            ),
        ],
        className="text-center",
    )

@app.callback(
    Output(
        "matchup-banner",
        "children"
    ),
    [
        Input(
            "team-a-dropdown",
            "value"
        ),
        Input(
            "team-b-dropdown",
            "value"
        ),
    ]
)
def update_matchup_banner(team_a, team_b):

    if not team_a or not team_b:
        return ""

    return dbc.Card(
        dbc.CardBody(
            html.Div(
                [
                    html.Img(
                        src=TEAM_INFO[team_a]["logo"],
                        style={"height": "100px"}
                    ),
                    html.H2(
                        f"{team_a} vs {team_b}",
                        style={"margin": "0 30px"}
                    ),
                    html.Img(
                        src=TEAM_INFO[team_b]["logo"],
                        style={"height": "100px"}
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                }
            )
        )
    )



@app.callback(
        Output(
            "prediction-explanation",
            "children"
        ),
        [
            Input(
                "team-a-dropdown",
                "value"
            ),
            Input(
                "team-b-dropdown",
                "value"
            ),
        ],
    )
def update_prediction_explanation(
        team_a,
        team_b,
    ):

          return dbc.Table(

    [

        html.Thead(

            html.Tr(

                [

                    html.Th(
                        "Factor"
                    ),

                    html.Th(
                        "Advantage"
                    ),

                ]

            )

        ),

        html.Tbody(

            [

                html.Tr([

                    html.Td(
                        "Win %"
                    ),

                    html.Td(
                        prediction[
                            "win_pct_diff"
                        ]
                    ),

                ]),

                html.Tr([

                    html.Td(
                        "PPG"
                    ),

                    html.Td(
                        prediction[
                            "ppg_diff"
                        ]
                    ),

                ]),

                html.Tr([

                    html.Td(
                        "Defense"
                    ),

                    html.Td(
                        prediction[
                            "papg_diff"
                        ]
                    ),

                ]),

                html.Tr([

                    html.Td(
                        "Point Differential"
                    ),

                    html.Td(
                        prediction[
                            "point_diff_advantage"
                        ]
                    ),

                ]),

            ]

        )

    ],

    bordered=True,
    striped=True,

) 
# Update Prediction Explanation
@app.callback(
    Output(
        "prediction-explanation",
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
def update_prediction_explanation(
    team_a,
    team_b,
):

    if not team_a or not team_b:
        return ""

    db = SessionLocal()

    try:

        prediction = predict_game(
            db,
            team_a,
            team_b,
        )
        return dbc.Table(

            [

                html.Thead(

                    html.Tr(
                        [
                            html.Th(
                                "Factor"
                            ),
                            html.Th(
                                "Advantage"
                            ),
                        ]
                    )

                ),

                html.Tbody(

                    [

                        html.Tr(
                            [
                                html.Td(
                                    "Win %"
                                ),
                                html.Td(
                                    prediction[
                                        "win_pct_diff"
                                    ]
                                ),
                            ]
                        ),

                        html.Tr(
                            [
                                html.Td(
                                    "PPG"
                                ),
                                html.Td(
                                    prediction[
                                        "ppg_diff"
                                    ]
                                ),
                            ]
                        ),

                        html.Tr(
                            [
                                html.Td(
                                    "Defense"
                                ),
                                html.Td(
                                    prediction[
                                        "papg_diff"
                                    ]
                                ),
                            ]
                        ),

                        html.Tr(
                            [
                                html.Td(
                                    "Point Differential"
                                ),
                                html.Td(
                                    prediction[
                                        "point_diff_advantage"
                                    ]
                                ),
                            ]
                        ),

                    ]

                )

            ],

            bordered=True,
            striped=True,

        )
  
    finally:
        db.close()
