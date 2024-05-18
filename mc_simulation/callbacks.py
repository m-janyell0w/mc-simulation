from dash.dependencies import Input, Output, State
from dash import dcc, callback
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go

from .app import app
from .simulation import MonteCarloSimulation


@app.callback(
    Output("simulation-graph-container", "children"),
    Input("submit-simu", "n_clicks"),
    State("num-simulations", "value"),
    State("num-days", "value"),
    State("initial-investment", "value"),
    State("dropdown-stock-ticker", "value"),
    State("monthly-investment", "value"),
    prevent_initial_call=True
)
def start_simulation(n_clicks, num_simulations, num_days, initial_investment, stock_ticker, monthly_investment):
    print("Starting simulation...")
    if n_clicks == 0:
        return html.Div("Simulation not started yet.")

    num_days = num_days * 22  # Convert number of months to trading days

    mcs = MonteCarloSimulation(
        symbol=stock_ticker,
        start_date='2010-01-01',
        end_date='2024-01-01',
        num_simulations=num_simulations,
        num_days=num_days,
        initial_investment=initial_investment,
        savings_rate=monthly_investment,
        savings_interval=22  # Monthly investment
    )
    results = mcs.run_simulation()

    if results is None:
        return html.Div("No data available for simulation.")

    fig = plot_simulation_results(results)

    fig.update_layout(
        title='Monte Carlo Simulation of Stock Portfolio',
        xaxis_title='Days',
        yaxis_title='Portfolio Value',
        template='plotly_dark'
    )

    return dcc.Graph(figure=fig)

def plot_simulation_results(results: np.ndarray, num_days: int, num_simulations: int):
    """
    Plot the results of the Monte Carlo simulation. This function plots the max and min simulations along with a subset
    of other simulations for comparison.
    """
    final_values = results[:, -1]
    max_index = final_values.argmax()
    min_index = final_values.argmin()

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=list(range(num_days + 1)), y=results[max_index], mode='lines', name='Max Simulation'))
    fig.add_trace(go.Scatter(x=list(range(num_days + 1)), y=results[min_index], mode='lines', name='Min Simulation'))

    num_to_plot = min(num_simulations, 50)
    indices = set([max_index, min_index])  # Ensure max and min are included
    while len(indices) < num_to_plot:
        indices.add(np.random.randint(num_simulations))

    for i in indices:
        if i != max_index and i != min_index:  # Avoid re-plotting max and min
            fig.add_trace(go.Scatter(x=list(range(num_days + 1)), y=results[i], mode='lines', name=f'Simulation {i+1}'))
    return fig


@callback(
    Output("test-output", "children"),
    Input("test-button", "n_clicks"),
    prevent_initial_call=True
)
def test_button(n_clicks):
    print(f"Button clicked {n_clicks} times.")
    return f"Button clicked {n_clicks} times."