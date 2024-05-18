import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from .global_components import SYMBOL_DROPDOWN_OPTIONS

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
                                dcc.Input(id="num-simulations", type="number", value=1000),
                            ],
                    ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Number of Months"),
                                dcc.Input(id="num-days", type="number", value=24),
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
                                dcc.Input(id="monthly-investment", type="number", value=1000),
                            ],
                        ),
                    ),
                    # add a button
                    dbc.Col(
                        html.Div(
                            [
                                html.Button("Get Data", id="get-data-button", n_clicks=0, className="button-class"),
                            ],
                            style={"margin-top": "25px", "align-items": "center"}
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Button("Start Simulation", id="submit-simu", n_clicks=0, className="button-class"),
                            ],
                            style={"margin-top": "25px"}
                        ),
                    ),
                    # add the output-div
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(id="output-div", children=html.Div("")),
                            ],
                        ),
                    ),
                    # new row
                    html.Div(
                        [
                            html.H5("Stock Ticker"),
                            # dcc.Input(id="stock-ticker", type="text", value="AAPL"),
                            dcc.Dropdown(id="dropdown-stock-ticker", options=SYMBOL_DROPDOWN_OPTIONS, value="AAPL", multi=False, 
                                            clearable=True, searchable=True),
                        ],
                    ),
                ])
            ],
    ),
    ],
)
# ],
# )
