# app/dashboard/layouts.py

from dash import html, dcc
import dash_bootstrap_components as dbc

from app.utils.nfl import (
    get_current_nfl_season,
    get_current_nfl_week,
)

CURRENT_SEASON = get_current_nfl_season()
CURRENT_WEEK = get_current_nfl_week()

layout = dbc.Container(

    [

        # ==================================================
        # HEADER
        # ==================================================

        dbc.Row(
            dbc.Col(
                [

                    html.H1(
                        "🏈 NFL Analytics Dashboard",
                        className="text-center mt-4"
                    ),

                    html.H5(
                        f"NFL Season {CURRENT_SEASON} — Week {CURRENT_WEEK}",
                        id="season-header",
                        className="text-center text-muted"
                    ),

                ]
            )
        ),

        html.Hr(),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Div("Season", className="fw-semibold mb-2 text-muted"),
                                    dcc.Dropdown(
                                        id="season-dropdown",
                                        placeholder="Select Season",
                                        options=[],
                                        value=None,
                                        clearable=False,
                                        searchable=False,
                                        className="season-dropdown",
                                    ),
                                ],
                                style={"maxWidth": "240px", "margin": "0 auto"},
                            ),
                        ],
                        className="py-3",
                    ),
                    className="border-0 shadow-sm rounded-3",
                ),
                xs=12,
                sm=8,
                md=5,
                lg=4,
                xl=3,
            ),
            justify="center",
            className="mb-4",
        ),

        # ==================================================
        # KPI CARDS
        # ==================================================

        dbc.Row(

            [

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Total Games"
                                ),
                                html.H2(
                                    id="games-card"
                                ),
                                
                            ]
                        )
                    ),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3",
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Teams"
                                ),
                                html.H2(
                                    id="teams-card"
                                ),
                            ]
                        )
                    ),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3",
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Avg Points/Game"
                                ),
                                html.H2(
                                    id="ppg-card"
                                ),
                            ]
                        )
                    ),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3",
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Home Win %"
                                ),
                                html.H2(
                                    id="home-card"
                                ),
                            ]
                        )
                    ),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3",
                ),

            ]

        ),

        # ==================================================
        # CHARTS
        # ==================================================

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="top-scoring-chart"
                                )
                            ]
                        )
                    ),

                    xs=12,
                    lg=6,

                ),

                dbc.Col(

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="win-percentage-chart"
                                )
                            ]
                        )
                    ),

                    xs=12,
                    lg=6,

                ),

            ],

            className="mb-5",

        ),

        html.Hr(),

        # ==================================================
        # TEAM EXPLORER
        # ==================================================
        html.Div(
            id="team-logo-container",
            className="text-center mb-3"
        ),
        
        html.H2(
            "🔍 Team Explorer",
            className="mb-4"
        ),

        dbc.Row(

            [
                dbc.Col(
                    dcc.Dropdown(
                        id="team-dropdown",
                        placeholder="Select Team",
                    ),
                    width=12,
                )
            ],

            className="mb-4",

        ),

        dbc.Row(

            [

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Wins"),
                                html.H3(id="team-wins"),
                            ]
                        )
                    ),
                    md=2,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Losses"),
                                html.H3(id="team-losses"),
                            ]
                        )
                    ),
                    md=2,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Ties"),
                                html.H3(id="team-ties"),
                            ]
                        )
                    ),
                    md=2,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("PPG"),
                                html.H3(id="team-ppg"),
                            ]
                        )
                    ),
                    md=2,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("PAPG"),
                                html.H3(id="team-papg"),
                            ]
                        )
                    ),
                    md=2,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Win %"),
                                html.H3(id="team-win-pct"),
                            ]
                        )
                    ),
                    md=2,
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6(
                                    "Point Diff"
                                ),
                                html.H3(
                                    id="team-point-diff"
                                ),
                            ]
                        )
                    ),
                    md=2,
                ),

            ],

            className="mb-4",

        ),

        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="team-trend-chart"
                    )
                ]
            ),
            className="mb-5",
        ),

        html.Hr(),

        # ==================================================
        # HEAD TO HEAD
        # ==================================================

        html.H2(
            "⚔️ Head-to-Head Comparison"
        ),
        html.Div(
            id="matchup-banner",
            className="mb-4"
        ),


        dbc.Row(

            [

                dbc.Col(
                    dcc.Dropdown(
                        id="team-a-dropdown",
                        placeholder="Team A",
                    ),
                    md=6,
                ),

                dbc.Col(
                    dcc.Dropdown(
                        id="team-b-dropdown",
                        placeholder="Team B",
                    ),
                    md=6,
                ),

            ],

            className="mb-3",

        ),

        dbc.Card(
            dbc.CardBody(
                html.Div(
                    id="comparison-table"
                )
            ),
            className="mb-3",
        ),

        dbc.Card(
            dbc.CardBody(

                [

                    html.H4(
                        "🏈 Game Prediction"
                    ),

                    html.Div(
                        id="prediction-output"
                    ),

                ]

            )
        ),


        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "🧠 Prediction Explanation"
                    ),

                    html.Div(
                        id="prediction-explanation"
                    ),
                ]
            ),
            className="mt-3",
        ),

        html.Hr(className="my-5"),

        # ==================================================
        # MODEL INSIGHTS
        # ==================================================

        html.H2(
            "🤖 Model Insights"
        ),

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Accuracy"
                                ),
                                html.H2(
                                    id="model-accuracy"
                                ),
                            ]
                        )
                    ),

                    md=6,

                ),

                dbc.Col(

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "ROC-AUC"
                                ),
                                html.H2(
                                    id="model-roc"
                                ),
                            ]
                        )
                    ),

                    md=6,

                ),

            ],

            className="mb-4",

        ),

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="confusion-matrix-chart"
                                )
                            ]
                        )
                    ),

                    md=6,

                ),

                dbc.Col(

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="roc-chart"
                                )
                            ]
                        )
                    ),

                    md=6,

                ),

            ],

            className="mb-4",

        ),

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="feature-importance-chart"
                                )
                            ]
                        )
                    ),

                    width=12,

                )

            ]

        ),

        html.Br(),
        html.Br(),

    ],

    fluid=True,

)