from dash.dependencies import Input, Output, State
from dash import dcc, callback, no_update
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go

# from .app import app
from .simulation import MonteCarloSimulation


@callback(
    Output("simulation-graph-container", "figure"),
    Input("submit-simu", "n_clicks"),
    State("num-simulations", "value"),
    State("num-months", "value"),
    State("initial-investment", "value"),
    Input("dropdown-stock-ticker", "value"),
    State("monthly-investment", "value"),
)
def run_simulation(n_clicks, num_simulations, num_months, initial_investment, stock_ticker, monthly_investment):
    
    fig = init_empty_fig(title=f"Monte Carlo Simulation for Asset: {stock_ticker}")
    if n_clicks == 0:
        return fig

    num_days = num_months * 22  # Convert number of months to trading days

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

    fig = plot_simulation_results(fig, results, num_days, num_simulations,
                                  stock_ticker)
    return fig

@callback(
    Output("simulation-progess-container", "children"),
    Input("submit-simu", "n_clicks"),
    Input("simulation-graph-container", "figure"),
    State("num-simulations", "value"),
    State("dropdown-stock-ticker", "value"),
    prevent_initial_call=True
)
def show_simulation_progress(n_clicks, graph_container, num_simulations, stock_ticker):
    if n_clicks == 0:
        return no_update
    if isinstance(graph_container, go.Figure):
        return html.Div(f"Simulation completed for {stock_ticker}.")

    return html.Div(f"Simlutation started. Running {num_simulations} simulations for {stock_ticker} ...")

def plot_simulation_results(fig: go.Figure, results: np.ndarray, num_days: int,
                            num_simulations: int, ticker_symbol: str, max_simulations=50):
    """
    Plot the results of the Monte Carlo simulation. This function plots the max and min simulations along with a subset
    of other simulations for comparison.
    """
    print("Create plot of simulation results.")
    final_values = results[:, -1]
    max_index = final_values.argmax()
    min_index = final_values.argmin()
    median_index = np.argsort(final_values)[len(final_values) // 2]    

    fig.add_trace(go.Scatter(x=list(range(num_days + 1)), y=results[max_index], mode='lines', name='Max'))
    fig.add_trace(go.Scatter(x=list(range(num_days + 1)), y=results[min_index], mode='lines', name='Min'))
    fig.add_trace(go.Scatter(x=list(range(num_days + 1)), y=results[median_index], mode='lines', name='Median'))

    num_to_plot = min(num_simulations, max_simulations)
    indices = set([max_index, min_index])  # Ensure max and min are included
    while len(indices) < num_to_plot:
        indices.add(np.random.randint(num_simulations))

    for i in indices:
        if i != max_index and i != min_index:  # Avoid re-plotting max and min
            fig.add_trace(go.Scatter(x=list(range(num_days + 1)), y=results[i], mode='lines', name=f'Simulation {i+1}'))
    
    fig.update_xaxes(tickvals=np.arange(0, num_days, 252), ticktext=np.arange(0, num_days//252))
    fig.update_yaxes(range=[0, 1.1 * results.max()])
    return fig


def init_empty_fig(xaxis_title="Years", yaxis_title="Portfolio Value",
                    title="Monte Carlo Simulation Results"):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
    )
    return fig

mc_simulation_callbacks = [
    run_simulation,
    show_simulation_progress,
    plot_simulation_results,
]

@callback(
    Output("test-output", "children"),
    Input("test-button", "n_clicks"),
    prevent_initial_call=True
)
def test_button(n_clicks):
    print(f"Button clicked {n_clicks} times.")
    return f"# Button clicked {n_clicks} times."
