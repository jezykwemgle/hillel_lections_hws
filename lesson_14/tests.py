import httpx


async def saving(url: str, data):
    with open(
        url.replace("https://", "").replace("/", "_").replace(".", "-"), "w"
    ) as file:
        file.write(data)


async def scraping(urls: list[str]):
    async with httpx.AsyncClient() as client:
        for url in urls:
            response = await client.get(url)
            if response.status_code == 200:
                await saving(url, response.json()["forms"][0]["name"])
            else:
                pass
