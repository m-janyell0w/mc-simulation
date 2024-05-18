import dash
import dash_core_components as dcc
import pandas as pd
import os
from mc_simulation.data_provider import FinanceDataReader, SymbolReader

finance_data_reader = FinanceDataReader()
symbol_reader = SymbolReader(filepaths=['mc_simulation/data/nasdaqlisted.txt', 'mc_simulation/data/otherlisted.txt'])
symbols = symbol_reader.read_symbols()
symbols = symbol_reader.process_symbols(symbols)

SYMBOL_DROPDOWN_OPTIONS = [{'label': f'{row["Security Name"]} ({row["ACT Symbol"]})',
                            'value': row["ACT Symbol"]} for index, row in symbols.iterrows()]
# print(SYMBOL_DROPDOWN_OPTIONS)