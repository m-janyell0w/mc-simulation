import numpy as np
import pandas as pd
from mc_simulation.data_provider import FinanceDataReader

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

    def run_simulation(self):
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

if __name__ == '__main__':
    # Configurable parameters
    symbol = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2021-01-01'
    num_simulations = 10
    num_days = 252
    initial_investment = 0
    savings_rate = 100  # Invest additional $100 every month
    savings_interval = 22  # Every 22 trading days

    mcs = MonteCarloSimulation(symbol, start_date, end_date, num_simulations, num_days, initial_investment, savings_rate, savings_interval)
    results = mcs.run_simulation()
    
    if results is not None:
        print("Simulation results:")
        print(results)
    else:
        print("Simulation failed.")