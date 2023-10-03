import random
import time
from threading import Thread
from typing import Generator

Rocket = tuple[str, float, int]


def random_delay() -> float:
    return random.random() * 5


def random_countdown() -> int:
    return random.randrange(5)


def launch_rocket(*_, rocket_name: str, delay: float, countdown: int):
    time.sleep(delay)  # wait
    for i in reversed(range(countdown)):  # 3, 2, 1 ...
        print(f"{i + 1}...")  # noqa:  T201
        time.sleep(1)
    print(f"Rocket {rocket_name} is launched")  # noqa:  T201


def create_rockets(
    n: int = 10000,
) -> Generator[Rocket, None, None]:  # 1 None - , 2 None - from return
    for i in range(1, n + 1):
        yield f"AA-{i}", random_delay(), random_countdown()


def run():
    rockets: Generator[Rocket, None, None] = create_rockets()
    # rockets = [("AA-12", random_delay(), random_countdown()),
    #            ("BB-12", random_delay(), random_countdown()),
    #            ("CC-12", random_delay(), random_countdown()),
    #            ]
    threads: list[Thread] = [
        Thread(
            target=launch_rocket,
            kwargs={
                "rocket_name": name,
                "delay": delay,
                "countdown": countdown,
            },
        )
        for name, delay, countdown in rockets
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    run()
