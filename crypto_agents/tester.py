from crypto_agents.monitor import CryptoMonitor
from crypto_agents.trader import TradingAgent

class MockCryptoMonitor(CryptoMonitor):
    """
    A mock version of the CryptoMonitor for testing purposes.
    It allows setting a manual price for a cryptocurrency.
    """
    def __init__(self):
        super().__init__()
        self.mock_prices = {}

    def set_price(self, crypto_id, price):
        self.mock_prices[crypto_id] = price

    def get_price(self, crypto_id, vs_currency='usd'):
        return self.mock_prices.get(crypto_id)

def run_simulation(trader, mock_monitor, crypto_id, price_series):
    """
    Runs a trading simulation for a given series of prices.
    """
    print(f"--- Starting simulation for {crypto_id} ---")
    print(f"Initial portfolio: {trader.portfolio}")

    for i, price in enumerate(price_series):
        print(f"\n--- Step {i+1}: Price = ${price} ---")
        mock_monitor.set_price(crypto_id, price)
        decision = trader.decide(crypto_id)
        print(f"Decision: {decision}")
        print(f"Portfolio: {trader.portfolio}")

    print("\n--- Simulation complete ---")


if __name__ == '__main__':
    # 1. Set up the agents
    mock_monitor = MockCryptoMonitor()
    # Stop-loss at 10%, gamble value of 0.5
    trader = TradingAgent(mock_monitor, stop_loss_pct=0.10, gamble_value=0.5)

    # 2. Define the price series for the simulation
    # This series will trigger a buy, a hold, and then a stop-loss sell.
    price_series = [
        100,  # Buy at 100
        105,  # Hold
        110,  # Hold
        95,   # Hold (5% drop, not enough for stop-loss)
        89,   # Sell (11% drop from 100, triggers 10% stop-loss)
        95,   # Stays sold
        120   # Stays sold (will not re-buy as sentiment is the same)
    ]

    # 3. Run the simulation
    run_simulation(trader, mock_monitor, 'fakecoin', price_series)

    # Example of how a re-buy might not happen
    print("\n--- Re-running with different sentiment to test re-buy ---")
    trader_high_gamble = TradingAgent(mock_monitor, stop_loss_pct=0.10, gamble_value=0.7)
    # This should not trigger a buy, as sentiment (0.6) < gamble_value (0.7)
    run_simulation(trader_high_gamble, mock_monitor, 'anothercoin', [100])
