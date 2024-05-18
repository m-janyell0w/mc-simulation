import pandas as pd
import yfinance as yf

class FinanceDataReader:

    def __init__(self) -> None:
        self.name = 'FinanceDataReader'

    def read_data(self, symbol: str, start: str = '2010-01-01', end: str = '2023-12-31', freq: str = '1d'):
        """
        Reads data from yahoo finance for the ticker symbol and stores them in a pandas DataFrames.
        """
        reader = yf.Ticker(symbol)
        stock_data = reader.history(start=start, end=end, period='1d')
        stock_info = reader.info
        return stock_data, stock_info
    
    def process_data(self, data: pd.DataFrame, columns: list[str] = ['Date', 'Close']):
        """
        Processes the data DataFrame by filtering out rows with NA.
        """
        data = data.dropna(subset=columns)
        # add a column for daily returns
        data['Return'] = data['Close'].pct_change()
        return data



class SymbolReader:

    def __init__(self, filepaths: list[str]) -> None:
        self.filepaths = filepaths

    def read_symbols(self, sep: str = '|'):
        """
        Reads symbols from NASDAQ lists stored under the filepaths and stores
        them in a list of pandas DataFrames.
        """
        symbols = pd.concat([pd.read_csv(filepath, sep=sep) for filepath in self.filepaths])
        return symbols
    
    def process_symbols(self, symbols: pd.DataFrame, columns: list[str] = ['ACT Symbol', 'Security Name', 'ETF']):
        """
        Processes the symbols DataFrame by filtering out unwanted symbols.
        """
        symbols = symbols.dropna(subset=["Security Name", "ACT Symbol"])
        return symbols[columns]