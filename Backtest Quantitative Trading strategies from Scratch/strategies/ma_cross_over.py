import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CrossOverBacktest:
    '''
        This package implements the well known Cross Over Strategy.
        There are four main methods. 
        1. Constructor
        2. Data Handler
        3. Backtest
        4. Results
        Inputs: capital, start_date, end_date, ticker, stock_series, short_term_trend, long_term_trend
        Output: dataframe with stock series, portfolio value, shares, holdings
    '''
    def __init__(self, capital, start_date, end_date, ticker, stock_series, short_term_trend, long_term_trend):

        # Outputs
        self.profits_df = pd.DataFrame()
        self.shares_df = pd.DataFrame()

        # Inputs
        self.capital = capital
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.stock_series = stock_series
        self.short_term_trend = short_term_trend
        self.long_term_trend = long_term_trend

        # Counters
        self.count_profit = 0
        self.count_loss = 0
        self.count_trade = 0

        # Avgs
        self.avg_positive_trade = 0
        self.avg_negative_trade = 0
        self.avg_trade = 0

        # Individual Trades
        self.profits = []        
        self.holdings = []      
        self.invested = []      # Capital - Holdins

        # Portfolio
        self.portfolio_value = None
        self.shares = None

        # Dataframes for price and performance
        self.prices_df = pd.DataFrame()
        self.results = None
        self.return_performance = None

        # Essential Price data
        self.open_price = None
        self.close_price = None
        self.profit_df = None

    def handle_data(self):
        pass

    def backtest(self):
        pass

    def get_results(self):
        pass