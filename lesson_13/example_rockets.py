import random
import time


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


def run():
    rockets = [
        ("AA-12", random_delay(), random_countdown()),
        ("BB-12", random_delay(), random_countdown()),
        ("CC-12", random_delay(), random_countdown()),
    ]
    for name, delay, countdown in rockets:  # розпаковка (*rocket)
        launch_rocket(rocket_name=name, delay=delay, countdown=countdown)


if __name__ == "__main__":
    start_time = time.perf_counter()
    run()
    end_time = time.perf_counter()
    total = end_time - start_time
    print(total)  # noqa:  T201
