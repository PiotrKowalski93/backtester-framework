# The Pipeline design pattern (also known as Chain of Command pattern) is a flexible way to handle a sequence of actions, where each handler 
# in the chain processes the input data and passes it to the next handler. 
# This pattern is commonly used in scenarios involving data processing, web scraping, or middleware systems.

import pandas as pd

# file from Udemy: Backtest Quantitative Trading strategies from Scratch
file_path = '.\\backtester_v2\\data\\EOD_FINAL.csv'

class Pipeline:
    '''
        Returns a dataframe of all traded securities on the major stock exchanges in the US.
        Input: starting date, ending date, field
        --> Field can be one of the following: 'open','high','low','close','volume','div','split','adj_open','adj_high','adj_low','adj_close','adj_volume'
    '''

    def __init__(self, start_date, end_date, field, file_path=file_path):
        self.start_date = start_date
        self.end_date = end_date
        self.field = field
        self.file_path = file_path

        self.pipe = pd.DataFrame()

    def make_pipeline(self):
        data = pd.read_csv(self.file_path, index_col=0)#, nrows=30000) # rows for now, remove in real world scenario

        # : - take all rows, and ('..','...') columns
        self.pipe = data.loc[:, ('symbol', 'time', self.field)]
        self.pipe.set_index(['time', 'symbol'], inplace=True)
        self.pipe.sort_index(inplace=True)

        # Unstuck the data for better visibility
        self.pipe = self.pipe.unstack(level='symbol')
        self.pipe = self.pipe.loc[self.start_date:self.end_date, self.field]
        #print(self.pipe)

        return self.pipe
    
    def get_prices(self, start_date, end_date, ticker):
        #print(self.pipe[ticker].loc[start_date:end_date])
        return self.pipe[ticker].loc[start_date:end_date]

# For testing purpouses.
# If name == main then file was started directly. We can use this place for basic tests
# else: code was imported as module
if __name__ == '__main__':
    print('Package is runnig locally')
    start_date = '2001-01-01'
    end_date = '2004-01-01'
    field = 'adj_close'

    test_pipe = Pipeline(start_date=start_date, end_date=end_date, field=field).make_pipeline()
    print(test_pipe)
# else:
    # print('Package exported')


