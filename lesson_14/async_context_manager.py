import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Product:
    id_prod: int
    name: str
    price: float


@dataclass
class UserConfig:
    payment_system: str


class PaymentSystem(ABC):
    @abstractmethod
    async def checkout(self, product: Product):
        """Perform the concrete checkout"""

    @abstractmethod
    async def end_connection(self):
        """Close connection"""


class PayPal(PaymentSystem):
    async def checkout(self, product: Product):
        print("Perform with PayPal")  # noqa: T201

    async def end_connection(self):
        print("Closing connection with PayPal")  # noqa: T201


class Stripe(PaymentSystem):
    async def checkout(self, product: Product):
        print("Perform with Stripe")  # noqa: T201

    async def end_connection(self):
        print("Closing connection with Stripe")  # noqa: T201


class PaymentSystemMeneger:
    def __init__(self, authenticated: bool, user_configuration: UserConfig):
        self.authenticated = authenticated
        self.user_configuration = user_configuration
        self._payment_system: PaymentSystem | None = None

    async def __aenter__(self) -> PaymentSystem:
        if self.authenticated is False:
            raise Exception("Please login")

        if self.user_configuration.payment_system == "paypal":
            self._payment_system = PayPal()
            return self._payment_system
        elif self.user_configuration.payment_system == "stripe":
            self._payment_system = Stripe()
            return self._payment_system

        raise Exception("Payment system is not supported")

    async def __aexit__(self, *args, **kwargs):
        if self._payment_system:
            await self._payment_system.end_connection()


async def main():
    user_config = UserConfig(payment_system="stripe")
    product = Product(id_prod=1, name="phone", price=4.0)
    async with PaymentSystemMeneger(
        authenticated=True, user_configuration=user_config
    ) as payment_system:
        await payment_system.checkout(product)


if __name__ == "__main__":
    asyncio.run(main())
