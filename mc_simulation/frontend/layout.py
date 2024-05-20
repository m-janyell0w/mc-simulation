import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from ..backend.global_components import SYMBOL_DROPDOWN_OPTIONS

APP_LAYOUT = html.Div(
    id="app-layout-container",
    style={"maxWidth": "95%", "margin": "auto", "padding": "10px"},
    children=[
        html.Div(
            id="input-container",
            children=[
                html.Br(),
                html.H2("Monte Carlo Simulation"),
                html.Hr(),
                html.H3("Simulate the Development of your Investment using simple Statistics 💸📈"),
                html.Br(),
            # add a row
            html.Div(
                className="row",
                children =
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Number of Simulations"),
                                dcc.Input(id="num-simulations", type="number", value=10),
                            ],
                    ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Number of Months"),
                                dcc.Input(id="num-months", type="number", value=12),
                            ],
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Initial Investment"),
                                dcc.Input(id="initial-investment", type="number", value=1000),
                            ],
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Monthly Investment"),
                                dcc.Input(id="monthly-investment", type="number", value=0),
                            ],
                        ),
                    ),
                    dbc.Col(
                            html.Div([
                                html.Button("Start Simulation", id="submit-simu", n_clicks=0),
                            ], style={"margin-top": "25px"}),
                        ),
                    html.Div(
                        [
                            html.Br(),
                            html.H5("Stock Ticker"),
                            # dcc.Input(id="stock-ticker", type="text", value="AAPL"),
                            dcc.Dropdown(id="dropdown-stock-ticker", options=SYMBOL_DROPDOWN_OPTIONS, value="URTH", multi=False, 
                                            clearable=True, searchable=True),
                        ]),
                    ]
                )
            ],
        ),
        html.Br(),
        html.Div(id="simulation-progess-container",
                 children="Simulation not started yet. Finalize your selection and click 'Start Simulation' to begin."),
        dcc.Graph(id="simulation-graph-container"),
        html.Br(),
        html.Div(id="simulation-summary-container",
                 children=""),
        html.Br(),
        html.Div(id="returns-analysis-container",
                 children=""),
    ],
)

TEST_LAYOUT = html.Div(
                    [dbc.Col(
                            [html.Button("TEST TESTS TEST", id="test-button"),
                            dcc.Markdown(id="test-output", children="# Initial output")]
                        )]
                    )