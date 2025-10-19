#TODO: Learn how to build and use portfolio for tests
# not working for now, still learning how to do it
class Portfolio:
    def __init__(self, init_cash):
        self.cash = init_cash           # Cash in portfolio
        self.position = 0               # Number of contracts
        self.avg_price = 0              # Avg price
        self.realized_pnl = 0           # Gain/Loss from closed positions
        self.unrealized_pnl = 0         # 
        self.history = []               # Equity history

    def update_position(self, side, price, qty):
        # We Buy - update avg price and position
        if side == "BUY":
            total_cost = self.avg_price * self.position + price * qty
            self.position += qty
            self.cash -= price * qty
            # This logic is flawed. We SELL even when we don't have.
            self.avg_price = total_cost / self.position
        # We sell
        elif side == "SELL" and self.position > 0:
            realized = (price - self.avg_price) * qty
            self.realized_pnl += realized
            self.position -= qty
            self.cash += price * qty

    def update_urealized_pn(self, current_price):
        self.unrealized_pnl = (current_price - self.avg_price) * self.position
        equity = self.cash + self.realized_pnl + self.unrealized_pnl
        self.history.append(equity)