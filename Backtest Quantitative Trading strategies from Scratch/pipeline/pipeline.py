# The Pipeline design pattern (also known as Chain of Command pattern) is a flexible way to handle a sequence of actions, where each handler 
# in the chain processes the input data and passes it to the next handler. 
# This pattern is commonly used in scenarios involving data processing, web scraping, or middleware systems.

import pandas as pd

# file from Udemy: Backtest Quantitative Trading strategies from Scratch
file_path = '.\Backtest Quantitative Trading strategies from Scratch\data\EOD_FINAL.csv'

class Pipeline:
    def __init__(self, start_date, end_date, field, file_path=file_path):
        self.start_date = start_date
        self.end_date = end_date
        self.field = field
        self.file_path = file_path

    def make_pipeline(self):
        data = pd.read_csv(self.file_path, index_col=0, nrows=3000000) # rows for now, remove in real world scenario
        
        # : - take all rows, and ('..','...') columns
        pipe = data.loc[:, ('symbol', 'time', self.field)]
        pipe.set_index(['time', 'symbol'], inplace=True)
        pipe.sort_indes(inplace=True)

        # Unstuck the data for better visibility
        pipe = pipe.unstack(level='symbol')
        pipe = pipe.loc[self.start_date:self.end_date, self.field]

if __name__ == '__main__':
    print('Package is runnig locally')
else:
    print('Package exported')


