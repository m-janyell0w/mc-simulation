from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash
from app import app
from layout import APP_LAYOUT


@app.callback(
    Output("output-div", "children"),
    Input("get-data-button", "n_clicks"),
    Input("num-simulations", "value"),
    State("num-days", "value"),
    State("initial-investment", "value"),
    State("stock-ticker", "value"),
)
def get_data(n_clicks, num_simulations, num_days, initial_investment, stock_ticker):
    # Perform simulation logic here
    # You can access the input values (num_simulations, num_days, initial_investment, stock_ticker) and perform the simulation
    # Return the output that you want to display in the "output-div" element
    print(f"Simulation started with {num_simulations} simulations.")
    return html.Div(f"Simulation started with {num_simulations} simulations.")


@app.callback(
    Output("output-div", "children"),
    Input("submit-simu", "n_clicks"),
    State("num-simulations", "value"),
    State("num-days", "value"),
    State("initial-investment", "value"),
    State("stock-ticker", "value"),
)
def start_simulation(n_clicks, num_simulations, num_days, initial_investment, stock_ticker):
    # Perform simulation logic here
    # You can access the input values (num_simulations, num_days, initial_investment, stock_ticker) and perform the simulation
    # Return the output that you want to display in the "output-div" element

    return html.Div(f"Simulation started with {num_simulations} simulations.")
