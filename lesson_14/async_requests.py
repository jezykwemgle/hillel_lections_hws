import asyncio
import sys
from time import perf_counter

BASE_URL = "https://pokeapi.co/api/v2"


def pokemons_requests(urls: list[str]):
    import requests

    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response)
    return results


def pokemons_grequests(urls: list[str]):
    import grequests

    results = grequests.map((grequests.get(url) for url in urls))
    return results


async def pokemons_httpx(urls: list[str]):
    import httpx

    results = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            response = await client.get(url)
            results.append(response)
    return results


def main():
    urls = [f"{BASE_URL}/pokemon/{i}" for i in range(1, 30)]

    match sys.argv[1]:
        case "requests":
            results = pokemons_requests(urls)
        case "grequests":
            results = pokemons_grequests(urls)
        case "httpx":
            results = asyncio.run(pokemons_httpx(urls))
        case _:
            raise Exception("Unknown")
    print(results)  # noqa: T201


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    end_time = perf_counter()
    total = end_time - start_time
    print(total)  # noqa: T201
