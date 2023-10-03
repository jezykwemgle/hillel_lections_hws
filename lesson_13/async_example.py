import asyncio
import sys
from typing import Coroutine

import grequests as gr
import httpx  # noqa: I201
import requests as r  # noqa: I201

# pokemons
BASE_URL = "https://pokeapi.co/api/v2/pokemon/{id_}"


def sync(urls: list[str]):
    for url in urls:
        _ = r.get(url)
    print(f"{len(urls)} pokemons received")  # noqa:  T201


def gsync(urls: list[str]):
    rs = (gr.get(u) for u in urls)
    gr.map(rs)
    print(f"{len(urls)} pokemons received")  # noqa:  T201


async def async_process(url: str):
    async with httpx.AsyncClient() as client:
        await client.get(url)


async def _run(*tasks: Coroutine):
    await asyncio.gather(*tasks)


def main():
    urls = [BASE_URL.format(id_=i) for i in range(1, int(sys.argv[2]) + 1)]

    if sys.argv[1] == "sync":
        sync(urls)
    elif sys.argv[1] == "gsync":
        gsync(urls)
    elif sys.argv[1] == "async":
        tasks: list[Coroutine] = [async_process(url) for url in urls]
        asyncio.run(_run(*tasks))
    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()
