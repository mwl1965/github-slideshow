import requests

class CryptoMonitor:
    """
    An agent that monitors cryptocurrency prices using the CoinGecko API.
    """
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_price(self, crypto_id, vs_currency='usd'):
        """
        Gets the current price of a cryptocurrency.

        :param crypto_id: The ID of the cryptocurrency (e.g., 'bitcoin').
        :param vs_currency: The currency to compare against (e.g., 'usd').
        :return: The price as a float, or None if an error occurs.
        """
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': crypto_id,
            'vs_currencies': vs_currency
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            return data[crypto_id][vs_currency]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from CoinGecko: {e}")
            return None
        except KeyError:
            print(f"Error: Invalid response format or cryptocurrency ID '{crypto_id}'.")
            return None

if __name__ == '__main__':
    monitor = CryptoMonitor()
    btc_price = monitor.get_price('bitcoin')
    if btc_price is not None:
        print(f"The current price of Bitcoin is ${btc_price}")

    eth_price = monitor.get_price('ethereum')
    if eth_price is not None:
        print(f"The current price of Ethereum is ${eth_price}")

    # Test with an invalid coin
    invalid_price = monitor.get_price('not-a-coin')
    if invalid_price is None:
        print("Correctly handled invalid coin.")
