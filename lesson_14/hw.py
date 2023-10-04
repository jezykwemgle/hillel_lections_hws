import asyncio
import logging

import aiohttp

logging.basicConfig(filename="scraper.log", filemode="w", level=logging.INFO)


class UrlGetter:
    def __init__(self, filename: str):
        self.filename = filename

    def get_urls(self):
        with open(self.filename, "r") as file:
            urls = [
                url.replace("\n", "")
                for url in file.read().split(",")
                if url.strip() != ""
            ]
            return urls


class Scraper:
    def __init__(self, urls, max_concurrent_requests=5):
        self.urls = urls
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.__queue = asyncio.Queue()

    async def scraper(self, session, url):
        try:
            async with self.semaphore:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.text()
                        await self.__queue.put(data)
                        logging.info("Put data into queue")
                    else:
                        logging.error(f"Bad status: {response.status}")
        except aiohttp.ClientError as e:
            logging.error(f"Error with a client: \n {e}")

    async def saving(self, filename: str):
        try:
            data = await self.__queue.get()
            logging.info("Get data from queue")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(data)
            logging.info("Data saved")
            self.__queue.task_done()
        except Exception as e:
            logging.error(f"Error while saving:\n {e}")

    async def scrap(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.scraper(session, url) for url in self.urls]
            logging.info("Created tasks for scraper")
            await asyncio.gather(*tasks)

            save_tasks = [
                self.saving(f"scraped_file{i}.json")
                for i in range(len(self.urls))
            ]
            logging.info("Created tasks for saving")
            await asyncio.gather(*save_tasks)


if __name__ == "__main__":
    urls = UrlGetter("urls.txt").get_urls()

    scraper = Scraper(urls)
    asyncio.run(scraper.scrap())
