import sys

import requests

API_KEY = "2GJ3JMTPUF7P8JIK"
BASE_URL: str = "https://www.alphavantage.co/"


def fetch_rate(from_currency: str, to_currency: str):
    """
    This function claims the currency rate information
    from the external service: Alphavantage
    """
    payload: str = (
        f"query?function=CURRENCY_EXCHANGE_RATE&"
        f"from_currency={from_currency.upper()}&"
        f"to_currency={to_currency.upper()}&"
        f"apikey={API_KEY}"
    )
    response: requests.Response = requests.get("".join([BASE_URL, payload]))
    data: dict = response.json()
    print(data)  # noqa: T201
    rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    return float(rate)  # noqa: T201


def main():
    from_currency, to_currency = sys.argv[1:3]
    rate: float = fetch_rate(from_currency, to_currency)
    print(f"{from_currency} --> {to_currency}: {rate}")  # noqa: T201


if __name__ == "__main__":
    main()
