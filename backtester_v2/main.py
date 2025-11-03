import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strategies.ma_cross_over import CrossOverBacktest
from pipelines.pipeline import Pipeline

import yfinance as yf

# 252 numer of avg business days
def annualized_return(df, freq=252):
    cumulative_return = (1 + df["returns"]).prod() - 1
    n_periods = len(df)
    return (1 + cumulative_return) ** (freq / n_periods) - 1

def annualized_volatility(df, freq=252):
    return df["returns"].std() * np.sqrt(freq)

def sharpe_ratio(df, risk_free_rate=0.04, freq=252):
    excess_return = df["returns"].mean() * freq - risk_free_rate
    return excess_return / (df["returns"].std() * np.sqrt(freq))

def drowdown(df):
    cumulative = (1 + df['returns']).cumprod()
    peak = cumulative.cummax()
    drowdown = (cumulative / peak - 1)
    return drowdown

def max_drawdown(df):
    cum_returns = (1 + df["returns"]).cumprod()
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    return drawdown.min() * 100

def rolling_correlation(first_df, second_df, window=60):
    return first_df["returns"].rolling(window).corr(second_df["returns"])

def spy_vs_russell():
    # For first time download:
    #spy = pd.DataFrame(yf.download("SPY", start="2000-01-01"))
    #spy.to_csv('.\\backtester_v2\\data\\spy.csv')

    # Load Spy
    spy = pd.read_csv('.\\backtester_v2\\data\\spy.csv', index_col=0)
    spy.index = pd.to_datetime(spy.index) 

    # For first time download:
    #russell = pd.DataFrame(yf.download("IWV", start="2000-01-01"))
    #russell.to_csv('.\\backtester_v2\\data\\russell.csv')

    # Load Russell
    russell = pd.read_csv('.\\backtester_v2\\data\\russell.csv', index_col=0)
    russell.index = pd.to_datetime(russell.index) 

    # Daily returns
    spy['returns'] = spy['Close'].pct_change()
    russell['returns'] = russell['Close'].pct_change()
    
    # Cumulative returns
    spy['cumulative_returns'] = (1 + spy['returns']).cumprod()
    russell['cumulative_returns'] = (1 + russell['returns']).cumprod()

    print(spy)
    print(russell)
    
    spy_grouped = spy.groupby(spy.index.year)
    russell_grouped = russell.groupby(russell.index.year)

    #TODO: 1) All metrics
    spy_annual_returns = spy_grouped.apply(annualized_return)
    russell_annual_returns = russell_grouped.apply(annualized_return)
    print(spy_annual_returns)
    print(russell_annual_returns)

    spy_annual_volatility = spy_grouped.apply(annualized_volatility)
    russell_annual_volatility = russell_grouped.apply(annualized_volatility)
    print(spy_annual_volatility)
    print(russell_annual_volatility)

    spy_sharpe_ratio = sharpe_ratio(spy)
    russell_sharpe_ratio = sharpe_ratio(russell)

    print(spy_sharpe_ratio)
    print(russell_sharpe_ratio)

    spy_max_drowdown = max_drawdown(spy)
    russell_max_drowdown = max_drawdown(russell)

    print(spy_max_drowdown)
    print(russell_max_drowdown)

    spy_vs_russell_rolling_col = rolling_correlation(spy, russell)
    
    #TODO: 2) Histograms for SPY and Russell
    plt.figure(figsize=(10,5))
    plt.plot(spy.index, spy['cumulative_returns'], label='SPY', linewidth=2)
    plt.plot(russell.index, russell['cumulative_returns'], label='Russell 3000', linewidth=2)
    plt.title('Cumulative Returns')
    plt.ylabel('Portfolio Value (Growth of $1)')
    plt.legend()
    plt.grid(True)
    plt.show()


    #TODO: 3) All plots on one dashboard

    #TODO: 4) Implement Momentum strategy with backtest 
    #TODO: 5) Implement Value Strategy with backtest
    #TODO: 6) Count measures as above for both and compare
    pass

if __name__ == "__main__":
    
   spy_vs_russell()






    # pipeline = Pipeline(start_date=start_date, end_date=None, field='adj_close')
    # pipe = pipeline.make_pipeline()
    # # Get tesla [date, price]
    # stock_prices = pipeline.get_prices(start_date = start_date, end_date = None, ticker = ticker)

    # # TESLA TRIAL FOR CROSS OVER STRATEGY
    # tesla_trial = CrossOverBacktest(start_date=start_date, end_date=end_date, ticker=ticker,
    #                                 capital=capital, short_term_trend=short_ma,long_term_trend=long_ma,
    #                                 stock_prices=stock_prices)
    # tesla_trial.handle_data(plot=False)
    # #print(tesla_trial.prices_df)

    # # TESLA BACKTESTING
    # tesla_trial.backtest()
    # tesla_trial.get_results()
    # print(tesla_trial.results)
