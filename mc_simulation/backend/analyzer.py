import numpy as np
import pandas as pd

class McResultsAnalyzer:
    def __init__(self, results: dict):
        self.results = self._dict_to_array(results)
        self.results_df = pd.DataFrame(results)
        self.final_values = self.results[:, -1]
    
    def get_annual_returns(self, results: np.ndarray, savings_rate: int, num_months: int) -> pd.DataFrame:
        """
        Compute the annual returns for each simulation based on the portfolio value
        at the end of each year (252 trading days). For not-yet-complete years, the last 
        value of the portfolio is used.
        """
        annual_values = self.get_annual_values(results, savings_rate, num_months)
        # print(f"annual values: {annual_values}")
        annual_returns = pd.DataFrame(
            annual_values,
            columns=[f"sim_{i}" for i in range(0, annual_values.shape[1])]
        )
        annual_returns = annual_returns.pct_change().dropna()
        annual_returns.index.name = 'Year'   
        return annual_returns
    
    def get_annual_values(self, results: np.ndarray, savings_rate: int, num_months: int) -> np.ndarray:
        """
        Compute the annual portfolio values for each simulation. Regular savings have to be
        subtracted from the portfolio value to get a estimate for the real annual portfolio
        growth.
        """
        annual_idx = list(range(len(results[0]))[::252])
        if annual_idx[-1] != len(results[0]) - 1: # account for incomplete years
            annual_idx.append(len(results[0]) - 1)
        annual_values = results[:, annual_idx].T
        if savings_rate == 0:
            return annual_values
        
        annual_savings = [savings_rate * 12] * annual_values.shape[1]
        if num_months % 12 != 0: # account for incomplete year
            annual_savings[-1] = savings_rate * (num_months % 12)

        for i in range(annual_values.shape[1]):
            annual_values[:, i] -= annual_savings[i]
        return annual_values

    @staticmethod
    def get_summary(result_data) -> dict:
        """
        Compute the summary statistics for the simulation data. This could be the final 
        portfolio values or alternatively the annual returns.
        The statistics are computed per row (axis=0), i.e., across simulations.
        """
        print(f"result data: {result_data}")
        summary = {}
        summary['median'] = np.median(result_data, axis=1)
        summary['mean'] = np.mean(result_data, axis=1)
        summary['std'] = np.std(result_data, axis=1)
        summary['min'] = np.min(result_data, axis=1)
        summary['max'] = np.max(result_data, axis=1)
        summary['5-th percentile'] = np.percentile(result_data, 5, axis=1)
        summary['95-th percentile'] = np.percentile(result_data, 95, axis=1)
        print(f"results summary: {summary}")
        return summary
    
    def _dict_to_array(self, results: list[dict], 
                      statistics_names: list[str]= ['median', 'min', 'max', 'mean', 'max-min']) -> np.ndarray:
        """
        Convert the dictionary of results to a numpy array. Format of the results
        is:
        [
           {'mode': 'lines', 'name': 'Max', 'x': [0, 1, 2, 3, ...], 'y': [100, 101, 102, 103, ...]},
           {'mode': 'lines', 'name': 'Min', 'x': [0, 1, 2, 3, ...], 'y': [100, 101, 102, 103, ...]},
            ...
        ]
        Note, that we are only interested in the simulation values, thus, all statistics names
        have to be removed.
        """
        results = [r for r in results if r['name'].lower() not in statistics_names]
        num_simulations = len(results)
        num_days = len(results[0]['x'])
        results_array = np.zeros((num_simulations, num_days))
        for i, result in enumerate(results):
            results_array[i] = result['y']
        return results_array
