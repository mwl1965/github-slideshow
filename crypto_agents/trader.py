from crypto_agents.monitor import CryptoMonitor

class TradingAgent:
    """
    An agent that makes buy/sell decisions for cryptocurrencies.
    """
    def __init__(self, monitor: CryptoMonitor, stop_loss_pct: float, gamble_value: float):
        self.monitor = monitor
        self.stop_loss_pct = stop_loss_pct
        self.gamble_value = gamble_value  # A value between 0 and 1
        self.portfolio = {}  # e.g., {'bitcoin': {'purchase_price': 50000}}

    def _get_market_sentiment(self):
        """
        A mock function to simulate market sentiment.
        In a real agent, this would be a complex calculation.
        """
        # For simulation, we'll return a value that allows trades.
        return 0.6

    def decide(self, crypto_id):
        """
        Makes a buy or sell decision for a given cryptocurrency.
        """
        current_price = self.monitor.get_price(crypto_id)
        if current_price is None:
            return "HOLD (could not get price)"

        # Sell logic
        if crypto_id in self.portfolio:
            purchase_price = self.portfolio[crypto_id]['purchase_price']
            price_change_pct = (current_price - purchase_price) / purchase_price
            if price_change_pct < -self.stop_loss_pct:
                del self.portfolio[crypto_id]
                return f"SELL {crypto_id} at ${current_price} (stop-loss triggered)"
            else:
                return f"HOLD {crypto_id} at ${current_price}"

        # Buy logic
        else:
            market_sentiment = self._get_market_sentiment()
            if market_sentiment > self.gamble_value:
                self.portfolio[crypto_id] = {'purchase_price': current_price}
                return f"BUY {crypto_id} at ${current_price}"
            else:
                return f"HOLD {crypto_id} (sentiment {market_sentiment} <= gamble value {self.gamble_value})"

if __name__ == '__main__':
    monitor = CryptoMonitor()
    # Stop-loss at 10% loss, gamble value of 0.5
    trader = TradingAgent(monitor, stop_loss_pct=0.10, gamble_value=0.5)

    print("--- First decision ---")
    decision = trader.decide('bitcoin')
    print(f"Decision: {decision}")
    print(f"Portfolio: {trader.portfolio}")

    print("\n--- Second decision (simulating price drop) ---")
    # Manually change the price in the portfolio for testing stop-loss
    if 'bitcoin' in trader.portfolio:
        trader.portfolio['bitcoin']['purchase_price'] = 130000 # Assume we bought at a higher price
    print(f"Updated portfolio for test: {trader.portfolio}")
    decision = trader.decide('bitcoin')
    print(f"Decision: {decision}")
    print(f"Portfolio: {trader.portfolio}")
