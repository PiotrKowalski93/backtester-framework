import pandas as pd

class DataFeed:
    def __init__(self, path : str):
        self.path = path
        self.data = None

    def load(self):
        self.data = pd.read_csv(self.path)
        return self.data
    
    # Return each row one by one
    def stream(self):
        for row in self.data.iterrows():
            yield row[1]