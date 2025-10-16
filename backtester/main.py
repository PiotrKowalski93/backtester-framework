from backtester.core.data_feed import DataFeed
from backtester.core.backtester import Backtester
from backtester.strategies.sma_strategy import SimpleMovingAverageStrategy
import matplotlib.pyplot as plt

if __name__ == "__main__":
    feed = DataFeed("./backtester/data/MMM.csv")
    strategy = SimpleMovingAverageStrategy(short_window=5, long_window=10, equity=10000)
    backtester = Backtester(data_feed=feed, strategy=strategy)
    backtester.run()

    print(strategy.trade_log)
    
    # print(portfolio.cash)
    # print(portfolio.position)
    # print(portfolio.history)

    # print(result["final_equity"])
    # print(result["trades"])

    # time =  [t[1] for t in result["trades"]]
    # equity = [t[2] for t in result["trades"]]

    # font1 = {'family':'serif','color':'blue','size':20}
    # font2 = {'family':'serif','color':'darkred','size':15}

    # plt.title("Strategy", fontdict = font1)
    # plt.xlabel("Time", fontdict = font2)
    # plt.ylabel("Equity", fontdict = font2)

    # plt.plot(time, equity)
    # plt.title("Equity Curve")
    # plt.show()

