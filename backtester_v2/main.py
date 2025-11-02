import pandas as pd
import numpy as np
from strategies.ma_cross_over import CrossOverBacktest
from pipelines.pipeline import Pipeline

if __name__ == "__main__":

    ticker = 'TSLA'
    start_date = '2017-01-01'
    end_date = '2021-10-29'
    capital = 100000
    long_ma = 13
    short_ma = 5

    pipeline = Pipeline(start_date=start_date, end_date=None, field='adj_close')
    pipe = pipeline.make_pipeline()
    # Get tesla [date, price]
    stock_prices = pipeline.get_prices(start_date = start_date, end_date = None, ticker = ticker)

    # TESLA TRIAL FOR CROSS OVER STRATEGY
    tesla_trial = CrossOverBacktest(start_date=start_date, end_date=end_date, ticker=ticker,
                                    capital=capital, short_term_trend=short_ma,long_term_trend=long_ma,
                                    stock_prices=stock_prices)
    tesla_trial.handle_data(plot=False)
    #print(tesla_trial.prices_df)

    # TESLA BACKTESTING
    tesla_trial.backtest()
    tesla_trial.get_results()
    print(tesla_trial.results)
