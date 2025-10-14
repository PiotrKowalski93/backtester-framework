# Simple Moving Avrage strategy

import pandas as pd
from backtester.core.strategy import IStrategy

class SimpleMovingAverageStrategy(IStrategy):
    def __init__(self, short_window, long_window, equity):
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []
        # 1 - long
        # -1 - short
        # 0 - flat
        self.position = 0
        self.equity = equity
        self.trade_log = []

    def on_tick(self, tick):
        price = tick['Close']
        self.prices.append(price)

        # Not enought data, need minimum one window
        if len(self.prices) < self.long_window:
            return

        # Short and long avg
        short_avg = pd.Series(self.prices[-self.short_window:]).mean()
        long_avg = pd.Series(self.prices[-self.long_window:]).mean()

        # Strategy logic
        if short_avg > long_avg and self.position <= 0:
            self.position = 1
            self.trade_log.append(("BUY", tick['Date'], price))
        elif short_avg < long_avg and self.position >= 0:
            self.position = -1
            self.trade_log.append(("SELL", tick['Date'], price))

        self.equity += self.position * (price - self.prices[-2])

    def on_finish(self):
        return {
            "final_equity": self.equity,
            "trades": self.trade_log
        }