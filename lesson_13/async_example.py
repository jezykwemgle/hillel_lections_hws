import grequests as gr
import requests as r  # noqa: I201

# pokemons
BASE_URL = "https://pokeapi.co/api/v2/pokemon/{id_}"


def sync(num: int):
    urls = [BASE_URL.format(id_=i) for i in range(1, num + 1)]
    for url in urls:
        _ = r.get(url)
    print(f"{len(urls)} pokemons received")  # noqa:  T201


def gsync(num: int):
    urls = [BASE_URL.format(id_=i) for i in range(1, num + 1)]
    rs = (gr.get(u) for u in urls)
    gr.map(rs)
    print(f"{len(urls)} pokemons received")  # noqa:  T201


def main():
    gsync(20)


if __name__ == "__main__":
    main()
