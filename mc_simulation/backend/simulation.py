import numpy as np
import pandas as pd
from mc_simulation.backend.data_provider import FinanceDataReader

class MonteCarloSimulation:
    def __init__(self, symbol, start_date, end_date, num_simulations, num_days, initial_investment, savings_rate=0, savings_interval=22):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.num_simulations = num_simulations
        self.num_days = num_days
        self.initial_investment = initial_investment if initial_investment > 0 else savings_rate
        self.savings_rate = savings_rate
        self.savings_interval = savings_interval
        self.data_retriever = FinanceDataReader()
        print(f"Monte Carlo Simulation initialized for {symbol} from {start_date} to {end_date} with {num_simulations} simulations.")
        
        stock_data, _ = self.data_retriever.get_data(symbol, start_date, end_date)
        self.data = stock_data

    def run_simulation(self) -> np.ndarray:
        if self.data is None or self.data.empty:
            print("No data available for simulation.")
            return None
        
        log_returns = np.log(1 + self.data['Return'].dropna())
        mean = log_returns.mean()
        std_dev = log_returns.std()

        results = np.zeros((self.num_simulations, self.num_days+1))

        for sim in range(self.num_simulations):
            print(f"Running simulation {sim+1}/{self.num_simulations}")
            prices = [self.initial_investment]
            for day in range(1, self.num_days + 1):
                if day % self.savings_interval == 0:
                    prices[-1] += self.savings_rate
                price_change = np.random.normal(mean, std_dev)
                prices.append(prices[-1] * np.exp(price_change))
            results[sim] = prices
        
        return results

class McResultsAnalyzer:
    def __init__(self, results: np.ndarray):
        self.results = results
        self.num_simulations, self.num_days = results.shape
        self.df = pd.DataFrame(results)
        self.df['mean'] = self.df.mean(axis=1)
        self.df['std'] = self.df.std(axis=1)
        self.df['min'] = self.df.min(axis=1)
        self.df['max'] = self.df.max(axis=1)
        self.df['final'] = self.df.iloc[:, -1]
        self.df['final_return'] = self.df['final'] / self.df[0] - 1
        self.df['final_return'] = self.df['final_return'].apply(lambda x: round(x*100, 2))
        self.df['final_return'] = self.df['final_return'].astype(str) + "%"
        self.df['final'] = self.df['final'].apply(lambda x: round(x, 2))
        self.df['final'] = self.df['final'].astype(str)
        self.df['mean'] = self.df['mean'].apply(lambda x: round(x, 2))
        self.df['mean'] = self.df['mean'].astype(str)
        self.df['std'] = self.df['std'].apply(lambda x: round(x, 2))
        self.df['std'] = self.df['std'].astype(str)
        self.df['min'] = self.df['min'].apply(lambda x: round(x, 2))
        self.df['min'] = self.df['min'].astype(str)
        self.df['max'] = self.df['max'].apply(lambda x: round(x, 2))
        self.df['max'] = self.df['max'].astype(str)
        print("Simulation results analyzed.")

    def get_summary(self) -> dict:
        summary = {}
        summary['mean'] = self.df['mean'].mean()
        summary['std'] = self.df['std'].mean()
        summary['min'] = self.df['min'].mean()
        summary['max'] = self.df['max'].mean()
        summary['final'] = self.df['final'].mean()
        summary['final_return'] = self.df['final_return'].mean()
        return summary

    def get_results(self) -> pd.DataFrame:
        return self.df
