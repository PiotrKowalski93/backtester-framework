import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

class CrossOverBacktest:
    '''
        This package implements the well known Cross Over Strategy.
        There are four main methods. 
        1. Constructor
        2. Data Handler
        3. Backtest
        4. Results
        Inputs: capital, start_date, end_date, ticker, stock_prices, short_term_trend, long_term_trend
        Output: dataframe with stock series, portfolio value, shares, holdings
    '''
    def __init__(self, capital, start_date, end_date, ticker, stock_prices, short_term_trend, long_term_trend):

        # Outputs
        self.profits_df = pd.DataFrame()
        self.shares_df = pd.DataFrame()

        # Inputs
        self.capital = capital
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
        self.stock_prices = stock_prices
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

    def handle_data(self, plot=False):
        # Main purpouse is to create signals based on the short and long term trend

        self.prices_df['stock_prices'] = self.stock_prices
        # Short Term mean
        self.prices_df['short_trend'] = self.stock_prices.rolling(self.short_term_trend).mean()
        # Long Term mean
        self.prices_df['long_trend'] = self.stock_prices.rolling(self.long_term_trend).mean()

        # where is like LINQ in C#. Return 1 if TRUE, 0 when FALSE
        positions_open = np.where(self.prices_df['short_trend'] > self.prices_df['long_trend'], 1, 0)

        self.prices_df['positions_open'] = positions_open
        # Nowe we have [0,1,1,1,1,0,0,0,1,1,1,...]
        # Consecutive 1's means that we are holding

        # Once we diff it
        # [0,1,0,0,0,0,-1,0,0,0,1,0,0,...]
        # now we know to buy on 1, and sell on -1
        self.prices_df['trade_open'] = self.prices_df['positions_open'].diff()

        # We need to know prices for our trades
        self.open_price = self.prices_df['stock_prices'][self.prices_df['trade_open'] == 1]
        self.close_price = self.prices_df['stock_prices'][self.prices_df['trade_open'] == -1]

        # We have to ensure that we do not have 1 at the end - we will buy and not close position
        if(len(self.open_price) > len(self.close_price)):
            
            last_trading_day = self.prices_df.index[-1]
            self.prices_df['positions_open'].loc[last_trading_day] = -1 # why?
            self.prices_df['trade_open'].loc[last_trading_day] = -1     

            # Adding extra trading day
            self.close_price.loc[last_trading_day] = self.prices_df['stock_prices'].loc[last_trading_day]

            # Determine profits
            self.profit_df = pd.DataFrame(self.close_price.values - self.open_price.values, index=self.close_price.index)

        elif (len(self.open_price) == len(self.close_price)):
            self.profit_df = pd.DataFrame(self.close_price.values - self.open_price.values, index=self.close_price.index)
            
        if plot:
            # TODO: Add plott later on
            pass

    def backtest(self):
        # Keeping track of shares and new positions
        self.shares = np.zeros(len(self.open_price))
        self.portfolio_value = np.zeros(len(self.open_price))

        # Open first trade
        self.count_trade += 1
        self.shares[0] = int(math.floor(self.capital / self.open_price.iloc[0]))
        actual_investment = round(self.shares[0] * self.open_price.iloc[0], 4)
        holding = self.capital - actual_investment

        # Close first trade
        profit_per_trade = round(self.shares[0] * self.profit_df.iloc[0,0], 4)
        if profit_per_trade > 0:
            self.count_profit += 1
        else:
            self.count_loss += 1

        # Calculate actual closing
        self.portfolio_value[0] = profit_per_trade + holding + actual_investment

        # Update step
        self.holdings.append(holding)
        self.profits.append(profit_per_trade)
        self.invested.append(actual_investment)

        # Now, we have initial conditions, then we can loop the rest
        for i in range(1, len(self.open_price) - 1):
            # Open trade
            self.count_trade += 1
            self.shares[i] = int(math.floor(self.portfolio_value[i-1] / self.open_price.iloc[i]))
            actual_investment = round(self.shares[i] * self.open_price.iloc[i], 4)
            holding = self.portfolio_value[i-1] - actual_investment

            # Close trade
            profit_per_trade = round(self.shares[i] * self.profit_df.iloc[i, 0], 4)
            if profit_per_trade > 0:
                self.count_profit += 1
            else:
                self.count_loss += 1

            # Calculate actual closing
            self.portfolio_value[i] = profit_per_trade + holding + actual_investment

            # TODO: Add every position with a date, it will be easier to put it together in get_results()
            # Update step
            self.holdings.append(holding)
            self.profits.append(profit_per_trade)
            self.invested.append(actual_investment)

    def get_results(self):
        # Amalgamation of backtest result into a final dataframe
        self.profit_df = pd.DataFrame(self.profits, columns=['profit_from_trade'])
        print('profit_df:')
        print(self.profit_df)

        # Portfolio, we want to have all days, not only those 
        portfolio_values_df = pd.DataFrame(self.portfolio_value, columns=['portfolio_value'], index=self.close_price.index).reindex(self.prices_df.index)
        #print(portfolio_values_df.to_string())

        self.shares_df = pd.DataFrame(self.shares, columns=['number_of_shares'], index=self.open_price.index).reindex(self.prices_df.index)

        print(self.holdings)
        print('   ')
        print(self.open_price)
        print('  ')
        #print(self.prices_df)

        holdings_df = pd.DataFrame(self.holdings, columns=['holdings']).reindex(self.open_price.index) #.reindex(self.prices_df.index)

        print('holdings:')
        print(holdings_df.to_string())

        # Final results df, axis=1 is date
        self.results = pd.concat([portfolio_values_df, self.shares_df, holdings_df], sort=True, axis=1)

        print('results:')
        print(self.results.to_string())

# For local fast testing purpouses
if __name__ == "__main__":
    np.random.seed(42)
    days = pd.date_range(start="2025-09-01", periods=80, freq="B")  # (Business days)
    prices = 100 + np.cumsum(np.random.normal(0.3, 1.5, size=80))
    stock_prices = pd.Series(prices, index=days, name="stock_prices")

    # TODO: Use pipeline
    s = CrossOverBacktest(1000, None, None, None, stock_prices, 3, 7)
    s.handle_data()
    s.backtest()
    s.get_results()