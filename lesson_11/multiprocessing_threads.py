from dataclasses import dataclass
from enum import Enum, auto
from threading import Thread  # good for IO-bound task
from time import sleep


# kitchen
class DishSize(str, Enum):
    S = auto()  # 'S'
    M = auto()  # 'M'
    L = auto()  # 'L'


# DishSize.S


@dataclass
class Dish:
    name: str
    size: DishSize
    ingredients: list[str]


# food = Dish('pizza', DishSize.S)


class Kitchen:
    @staticmethod
    def heat(dish: Dish):
        """
        This function heat the meal. It is IO-bound task.
        We should wait until meal is warm.
        """
        print(f"{dish.name} started hitting.")  # noqa: T201
        sleep(3)  # IO-bound
        print(f"The {dish} is warm.\n")  # noqa: T201

        # IO bound задачі це очікування чогось

    @staticmethod
    def cook(dish: Dish):
        """
        This function cooc the meal. It is CPU-bound task.
        We should cook the meal.
        """
        print(f"{dish.name} started cooking.")  # noqa: T201
        _ = [i for i in range(120000000)]  # CPU-bound
        print(f"The {dish} is ready.")  # noqa: T201

        # CPU bound задачі це просто код який виконується послідовно,
        # строка за строкою


pizza = Dish(
    name="Margarita",
    size=DishSize.S,
    ingredients=["cheese", "sauce", "tomato"],
)

salad = Dish(
    name="Caesar",
    size=DishSize.M,
    ingredients=["chicken", "sauce", "salad", "chips", "tomato"],
)

dishes = [pizza, salad]

# concurrent execution
threads = [
    Thread(
        target=Kitchen.heat,
        args=(dish,),
    )
    for dish in dishes
]
for thread in threads:
    thread.start()  # Розпочати діяльність нового потоку.
    # Він має бути викликаний щонайбільше один раз на об’єкт потоку.
    # Він організовує виклик методу run() об’єкта в
    # окремому потоці керування.

for thread in threads:
    thread.join()  # Зачекайте, поки потік завершиться. Це блокує потік,
    # що викликає, доки потік, чий метод join()
    # викликається, не завершиться (звичайно або через необроблений виняток),
    # або доки не настане додатковий
    # час очікування.
