import numpy as np
import plotly.graph_objs as go

class Plotter:


    def plot_simulation_results(self, fig: go.Figure, results: np.ndarray, num_days: int,
                            num_simulations: int, ticker_symbol: str, max_simulations=20):
        """
        Plot the results of the Monte Carlo simulation. This function plots the max and min simulations along with a subset
        of other simulations for comparison.
        """
        final_values = results[:, -1]
        max_index = final_values.argmax()
        min_index = final_values.argmin()
        median_index = np.argsort(final_values)[len(final_values) // 2]    

        fig.add_trace(go.Scatter(x=list(range(num_days + 1)), y=results[median_index], mode='lines', name='Median', line=dict(color='black', width=3)))
        self.add_shaded_area(fig, results, num_days, max_index, min_index)

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
    def plot_result_distribution(self, fig: go.Figure, results: np.ndarray,
                                 num_days: int, kind: str = "hist"):
        """
        Plot the distribution of the final values of the simulation results.
        """
        final_values = results[:, -1]
        fig = go.Figure()
        if kind == "hist":
            fig.add_trace(go.Histogram(x=final_values, nbinsx=20))
        elif kind == "box":
            fig.add_trace(go.Box(y=final_values))
        fig.update_layout(
            title="Distribution of Final Portfolio Values",
            xaxis_title="Portfolio Value",
            yaxis_title="Frequency"
        )
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

    def add_shaded_area(self, fig: go.Figure, results: np.ndarray,
                        num_days: int, max_index: int, min_index: int):
        """
        Add a shaded area to the plot between the max and min value of simulation values.
        """
        fig.add_trace(go.Scatter(
            x=list(range(num_days + 1)) + list(range(num_days + 1))[::-1],
            y=list(results[max_index]) + list(results[min_index])[::-1],
            fill='toself',
            fillcolor='rgba(0,120,90,0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Max-Min',
        ))