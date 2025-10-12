import yfinance as yf
import pandas as pd

# Read csv with S&P 500 Symbols
# TODO: download updated list every run
symbols = pd.read_csv('data/symbols_sp500.csv')['Symbol']
print(symbols)

# Calculate Start and End Date - 5 years
end_date = '2025-10-12'
start_date = pd.to_datetime(end_date) - pd.DateOffset(365*5)

# Prepare .csv per symbol ex: AAPL.csv
for symbol in symbols[:2]:
    data = yf.download(tickers=symbol,
                   start=start_date,
                   end=end_date,
                   multi_level_index=False,
                   auto_adjust=False)
    data.to_csv(f'data/{symbol}.csv')

