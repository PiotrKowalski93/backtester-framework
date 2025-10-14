class Portfolio:
    def __init__(self, init_cash):
        self.cash = init_cash      # Cash in portfolio
        self.position = 0               # Number of contracts
        self.avg_price = 0              # Avg price
        self.realized_pnl = 0           # Gain/Loss from closed positions
        self.history = 0                # Equity history

    def update_position(self, side, price, qty):
        # We Buy - update avg price and position
        if side == "BUY":
            total_cost = self.avg_price * self.position + price * qty

            self.position += qty
            self.cash -= price * qty
            self.avg_price = total_cost / self.position
        # We sell
        elif side == "SELL":
            self.position -= qty
            self.cash += price * qty
            #TODO: finish implementation

    def update_urealized_pn(self, current_price):
        #TODO: implement    