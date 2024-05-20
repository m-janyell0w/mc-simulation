import pandas as pd
import yfinance as yf

class FinanceDataReader:

    def __init__(self) -> None:
        self.name = 'FinanceDataReader'

    def get_data(self, symbol: str, start: str = '2010-01-01', end: str = '2023-12-31', freq: str = '1d')-> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Retrieves data for the ticker symbol from Yahoo Finance and processes it.
        """
        stock_data, stock_info = self.read_data(symbol, start, end, freq)
        stock_data = self.process_data(stock_data)
        return stock_data, stock_info

    def read_data(self, symbol: str, start: str = '2010-01-01', end: str = '2023-12-31', freq: str = '1d')-> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Reads data from yahoo finance for the ticker symbol and stores them in a pandas DataFrames.
        """
        try:
            reader = yf.Ticker(symbol)
            stock_data = reader.history(start=start, end=end, interval=freq)
            stock_info = reader.info
            return stock_data, stock_info
        except Exception as e:
            print(f"Error retrieving data for {symbol}: {e}")
            return pd.DataFrame(), pd.DataFrame()
            
    def process_data(self, data: pd.DataFrame, dropna_columns: list[str] = ['Close'],
                     close_column: str = 'Close'):
        """
        Processes the data DataFrame by filtering out rows with NA.
        """
        if not data.empty:
            data = data.dropna(subset=dropna_columns)
            # add a column for daily returns
            data['Return'] = data[close_column].pct_change()
        return data



class SymbolReader:

    def __init__(self, filepaths: list[str]) -> None:
        self.filepaths = filepaths

    def read_symbols(self, sep: str = '|'):
        """
        Reads symbols from NASDAQ lists stored under the filepaths and stores
        them in a list of pandas DataFrames.
        """
        all_symbols = []
        for filepath in self.filepaths:
            try:
                symbols = pd.read_csv(filepath, sep=sep)
                all_symbols.append(symbols)
            except Exception as e:
                print(f"Error reading file {filepath}: {e}")
        return pd.concat(all_symbols, ignore_index=True) if all_symbols else pd.DataFrame()
    
    def process_symbols(self, symbols: pd.DataFrame, columns: list[str] = ['ACT Symbol', 'Security Name', 'ETF']):
        """
        Processes the symbols DataFrame by filtering out unwanted symbols.
        """
        if not symbols.empty:
            symbols = symbols.dropna(subset=["Security Name", "ACT Symbol"])
            return symbols[columns]
        else:
            print("No symbols to process.")
            return pd.DataFrame()
        

if __name__ == '__main__':
    # Test FinanceDataReader
    fdr = FinanceDataReader()
    stock_data, stock_info = fdr.get_data('AAPL', '2020-01-01', '2020-02-01')
    if stock_data is not None:
        print("Processed Stock Data:")
        print(stock_data.head())
    if stock_info is not None:
        print("\nStock Info:")
        print(stock_info)
