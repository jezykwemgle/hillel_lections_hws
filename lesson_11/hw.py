import os
import threading
from multiprocessing import Process
from threading import Thread
from time import perf_counter

import requests


class Helper:
    # CPU-bound task (heavy computation)
    @staticmethod
    def encrypt_file(path: str):
        start_time = perf_counter()
        print(  # noqa:  T201
            f"Processing file  from {path} in process {os.getpid()}"
        )  # noqa:  T201
        # Simulate heavy computation by sleeping for a while
        _ = [i for i in range(100_000_000)]
        end_time = perf_counter()
        encryption_time = end_time - start_time
        return encryption_time

    # I/O-bound task (downloading image from URL)
    @staticmethod
    def download_image(image_url):
        start_time = perf_counter()
        print(  # noqa:  T201
            f"Downloading image from {image_url} "
            f"in thread {threading.current_thread().name}"
        )
        response = requests.get(image_url)
        with open("image.jpg", "wb") as f:
            f.write(response.content)
        end_time = perf_counter()
        download_time = end_time - start_time
        return download_time


if __name__ == "__main__":
    try:
        start_time = perf_counter()
        encryption_process = Process(
            target=Helper.encrypt_file, args=("rockyou.txt",)
        )
        encryption_process.start()

        downloading_thread = Thread(
            target=Helper.download_image,
            args=("https://picsum.photos/1000/1000",),
        )
        downloading_thread.start()

        encryption_process.join()
        downloading_thread.join()

        end_time = perf_counter()
        total = end_time - start_time

        encryption_counter = Helper.encrypt_file("rockyou.txt")
        download_counter = Helper.download_image(
            "https://picsum.photos/1000/1000"
        )

        print(  # noqa:  T201
            f"Time taken for encryption task: {encryption_counter}, "
            f"I/O-bound task: {download_counter}, "
            f"Total: {total} seconds"
        )
    except Exception as e:
        print(f"Error occurred: {e}")  # noqa:  T201
