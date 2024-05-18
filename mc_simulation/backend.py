import pandas as pd
import yfinance as yf

from .data_provider import FinanceDataReader

class Backend:
    def __init__(self) -> None:
        self.name = 'Backend'
        self.finance_data_reader = FinanceDataReader()
    
    def get_stock_data(self, symbol: str, start: str = '2010-01-01', end: str = '2023-12-31', freq: str = '1d',
                       columns: list[str] = ['Date', 'Close']):
        """
        Reads data from yahoo finance for the ticker symbol and stores them in a pandas DataFrames.
        """
        stock_data, _ = self.finance_data_reader.read_data(symbol, start, end, freq)
        stock_data = self.finance_data_reader.process_data(stock_data, columns)
        return stock_data
    
    def simulate(self, stock_data: pd.DataFrame, num_simulations: int, num_days: int, initial_investment: float):
        """
        Simulates the stock price for the given number of simulations and days.
        """
        # get the last stock price
        last_stock_price = stock_data['Close'].iloc[-1]
        # create a new DataFrame to store the simulation results
        simulation_results = pd.DataFrame()
        # loop through the number of simulations
        for i in range(num_simulations):
            # create a list to store the simulation results
            simulation = []
            # set the initial investment
            investment = initial_investment
            # loop through the number of days
            for j in range(num_days):
                # get the stock price for the current day
                stock_price = stock_data['Close'].iloc[j]
                # calculate the daily return
                daily_return = stock_data['Return'].iloc[j]
                # calculate the new investment value
                investment = investment * (1 + daily_return)
                # add the investment value to the simulation results
                simulation.append(investment)
            # add the simulation results to the simulation DataFrame
            simulation_results[i] = simulation
        # calculate the final investment value for each simulation
        simulation_results['Final Investment'] = simulation_results.iloc[-1]
        return simulation_results

