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
        self.profits = pd.Series(dtype='float64')        
        self.holdings = pd.Series(dtype='float64')     
        self.invested = pd.Series(dtype='float64')

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
            
            # df.loc[row_indexer, "col"] = values modyfi orginal object
            self.prices_df.loc[last_trading_day, "positions_open"] = -1
            self.prices_df.loc[last_trading_day, "trade_open"] = -1

            # Adding extra trading day
            self.close_price.loc[last_trading_day] = self.prices_df['stock_prices'].loc[last_trading_day]

            # Determine profits
            self.profit_df = pd.DataFrame(self.close_price.values - self.open_price.values, index=self.close_price.index)

        elif (len(self.open_price) == len(self.close_price)):
            self.profit_df = pd.DataFrame(self.close_price.values - self.open_price.values, index=self.close_price.index)
            
        if plot:
            plt.figure(figsize=(12, 8))

            # Plot the closing price
            plt.plot(self.prices_df['stock_prices'], color='black', lw=2.)

            # Plot the short and long moving averages
            plt.plot(self.prices_df[['short_trend', 'long_trend']], lw=2.)

            # Plot the buy signals
            plt.plot(self.prices_df.stock_prices[self.prices_df.trade_open == 1], '^', markersize=8, color='m', label='buy signal')

            # Plot the sell signals
            plt.plot(self.prices_df.stock_prices[self.prices_df.trade_open == -1], 'v', markersize=8, color='k', label='sell signal')
            plt.legend(['price', 'MA_'+str(self.short_term_trend), 'MA_'+str(self.long_term_trend), 'Buy Signal', 'Sell Signal'], loc='best')

            plt.show()
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

        current_step_date = self.open_price.index[0]
        self.holdings[current_step_date] = holding
        self.profits[current_step_date] = profit_per_trade
        self.invested[current_step_date] = actual_investment

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

            # Update step
            current_step_date = self.open_price.index[i]
            self.holdings[current_step_date] = holding
            self.profits[current_step_date] = profit_per_trade
            self.invested[current_step_date] = actual_investment

        # print(self.holdings)
        # print(self.profits)
        # print(self.invested)

    def get_results(self):
        self.profits_df = pd.DataFrame(self.profits, columns=['profit_from_trade'])
        # create the portfolio data frame, we reset the index to all the trading days, same goes for the other metrics
        port_val_df = pd.DataFrame(self.portfolio_value, index=self.close_price.index, columns=['portfolio_value']).reindex(index=self.prices_df.index)
        self.shares_df = pd.DataFrame(self.shares, index=self.open_price.index, columns=['shares']).reindex(index=self.prices_df.index)
        holding_df = pd.DataFrame(self.holdings, index=self.open_price.index, columns=['holdings']).reindex(index=self.prices_df.index)

        # concatenating them together
        self.results = pd.concat([port_val_df, self.shares_df, holding_df, self.prices_df.stock_price], sort=True, axis=1)
        # print("\t \t {0} ".format(self.results))
        # if no trades are placed on the first day, we set it to 0, which will help with forward filling
        for i in range(len(self.close_price.index)):
            open_ = self.open_price.index[i]
            close_ = self.close_price.index[i]
            self.results.shares.loc[open_: close_].fillna(method='ffill', inplace=True)
            self.results.holdings.loc[open_: close_].fillna(method='ffill', inplace=True)

        self.results.portfolio_value.loc[:self.open_price.index[0]].fillna(self.capital, inplace=True)
        # portfolio_value = shares * stock_price + what ever we are holding
        self.results.portfolio_value = self.results.portfolio_value.fillna(self.results.shares * self.results.stock_price)
        self.results.portfolio_value = self.results.portfolio_value + self.results.holdings
        self.results.portfolio_value.fillna(method='ffill', inplace=True)
        self.results.shares.fillna(0, inplace=True)
        self.results.holdings.fillna(0, inplace=True)

        self.count_loss = self.count_trade - self.count_profit
        self.average_trade_val = self.profits_df.profit_from_trade.mean()

        self.avg_pos_trades = self.profits_df.profit_from_trade[self.profits_df.profit_from_trade > 0].mean()
        self.avg_neg_trades = self.profits_df.profit_from_trade[self.profits_df.profit_from_trade < 0].mean()

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