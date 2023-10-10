import argparse
import asyncio
import csv

import aiohttp
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


async def fetch_currency_exchange_rate(
    schema: AlphavantageCurrencyExchangeRequest, session
) -> str:
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
    async with session.get("".join([BASE_URL, payload])) as raw_response:
        raw_response = await raw_response.json()
        response = AlphavantageCurrencyExchangeResponse(**raw_response)
    return (
        f"{response.results.currency_from} --> "
        f"{response.results.currency_to}: "
        f"{response.results.currency_rate}"
    )


def get_currency_list(filename):
    currency = []
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            currency.append(row[0])
    return currency[1:]


def arg_parser():
    currency = get_currency_list("currency_list.csv")
    parser = argparse.ArgumentParser(
        prog="Exchange Rates",
        description="This program helps to get exchange rates",
    )
    parser.add_argument(
        "currency_from", choices=[c.lower() for c in currency], nargs="+"
    )
    parser.add_argument(
        "--target", choices=[c.lower() for c in currency], nargs="+"
    )
    return parser.parse_args()


async def main():
    args: argparse.Namespace = arg_parser()
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_currency_exchange_rate(
                AlphavantageCurrencyExchangeRequest(
                    currency_from=currency_from, currency_to=args.target[0]
                ),
                session,
            )
            for currency_from in args.currency_from
        ]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    print(asyncio.run(main()))  # noqa
