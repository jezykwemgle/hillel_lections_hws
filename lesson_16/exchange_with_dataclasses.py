import sys

import requests  # noqa
from pydantic import BaseModel, Field  # noqa

API_KEY = "2GJ3JMTPUF7P8JIK"
BASE_URL: str = "https://www.alphavantage.co/"


class AlphavantageCurrencyExchangeRequest(BaseModel):
    currency_from: str
    currency_to: str


class AlphavantageCurrencyExchangeResults(BaseModel):
    currency_from: str = Field(alias="1. From_Currency Code")
    currency_to: str = Field(alias="3. To_Currency Code")
    currency_rate: str = Field(alias="5. Exchange Rate")


class AlphavantageCurrencyExchangeResponse(BaseModel):
    results: AlphavantageCurrencyExchangeResults = Field(
        alias="Realtime Currency Exchange Rate"
    )


def fetch_currency_exchange_rate(
    schema: AlphavantageCurrencyExchangeRequest,
) -> AlphavantageCurrencyExchangeResponse:
    """
    This function claims the currency rate information
    from the external service: Alphavantage
    """
    payload: str = (
        f"query?function=CURRENCY_EXCHANGE_RATE&"
        f"from_currency={schema.currency_from.upper()}&"
        f"to_currency={schema.currency_to.upper()}&"
        f"apikey={API_KEY}"
    )
    raw_response: requests.Response = requests.get(
        "".join([BASE_URL, payload])
    )
    response = AlphavantageCurrencyExchangeResponse(**raw_response.json())
    return response


def main():
    currency_from, currency_to = sys.argv[1:3]
    schema = AlphavantageCurrencyExchangeRequest(
        currency_from=currency_from, currency_to=currency_to
    )
    result = fetch_currency_exchange_rate(schema=schema)
    print(  # noqa: T201
        f"{result.currency_from} --> " f"{result.currency_to}: {result.rate}"
    )


if __name__ == "__main__":
    main()
