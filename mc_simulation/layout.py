import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# use bootstrap styles
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


APP_LAYOUT = html.Div(
    id="app-layout-container",
    children=[
        # Banner
        html.Div(
            id="app-banner",
            children=[
                html.Br(),
                html.H2("Monte Carlo Simulation"),
                html.Hr(),
                html.H3("Simulate the development of stock markets using Statistics!"),
                html.Br(),
            # add a row
            html.Div(
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
                                html.H5("Stock Ticker"),
                                dcc.Input(id="stock-ticker", type="text", value="AAPL"),
                            ],
                        ),
                    ),
                    # add a button
                    dbc.Col(
                        html.Div(
                            [
                                html.Button("Get Data", id="get-data-button", n_clicks=0),
                            ],
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Button("Start Simulation", id="submit-simu", n_clicks=0),
                            ],
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


                ],
            className="row",
    ),
    ],
    ),
],
)
