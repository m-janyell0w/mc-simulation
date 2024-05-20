import numpy as np
import plotly.graph_objs as go

class Plotter:

    @staticmethod
    def plot_simulation_results(fig: go.Figure, results: np.ndarray, num_days: int,
                            num_simulations: int, ticker_symbol: str, max_simulations=50):
        """
        Plot the results of the Monte Carlo simulation. This function plots the max and min simulations along with a subset
        of other simulations for comparison.
        """
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

    @staticmethod
    def init_empty_fig(xaxis_title="Years", yaxis_title="Portfolio Value",
                        title="Monte Carlo Simulation Results"):
        """
        Inititalize an empty graph-objects figure for plotting the simulation
        results.
        """
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
        )
        return fig
