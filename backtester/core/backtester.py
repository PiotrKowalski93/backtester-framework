# Logic that runs simulation for full set of data

class Backtester:
    def __init__(self, data_feed, strategy):
        self.data_feed = data_feed
        self.strategy = strategy

    def run(self):
        data = self.data_feed.load()
        
        for tick in self.data_feed.stream():
            self.strategy.on_tick(tick)

        result = self.strategy.on_finish()
        return result