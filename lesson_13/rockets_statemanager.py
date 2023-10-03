import heapq
import random
import time
from enum import Enum, auto
from typing import Generator

Rocket = tuple[str, float, int]


class Op(Enum):  # operation
    WAIT = auto()
    STOP = auto()


def sleep(delay):
    yield Op.WAIT, delay


def now():
    return time.time()


def random_delay() -> float:
    return random.random() * 5


def random_countdown() -> int:
    return random.randrange(5)


def launch_rocket(*_, rocket_name: str, delay: float, countdown: int):
    yield from sleep(delay)  # wait
    for i in reversed(range(countdown)):  # 3, 2, 1 ...
        print(f"{i + 1}...")  # noqa:  T201
        yield from sleep(1)
    print(f"Rocket {rocket_name} is launched")  # noqa:  T201


def create_rockets(
    n: int = 10000,
) -> Generator[Rocket, None, None]:  # 1 None - , 2 None - from return
    for i in range(1, n + 1):
        yield f"AA-{i}", random_delay(), random_countdown()


def run():
    rockets: Generator[Rocket, None, None] = create_rockets()
    work = [
        (
            now(),
            index,
            launch_rocket(rocket_name=name, delay=delay, countdown=countdown),
        )
        for index, (name, delay, countdown) in enumerate(rockets)
    ]

    while work:
        step_at, index, launch = heapq.heappop(work)
        wait = step_at - now()

        if wait > 0:
            time.sleep(wait)

        try:
            op, arg = launch.send(None)
        except StopIteration:
            continue
        if op == Op.WAIT:
            step_at = now()
            heapq.heappush(work, (step_at, index, launch))
        else:
            assert op is Op.STOP


if __name__ == "__main__":
    run()
