import asyncio as asy


async def foo():
    await asy.sleep(1)
    print("i`m foo")  # noqa:  T201


async def bar():
    await asy.sleep(2)
    print("i`m bar")  # noqa:  T201


async def main():
    tasks = [foo(), bar()]
    results = await asy.gather(*tasks)  # noqa:  F841

    # await foo()
    # await bar()


if __name__ == "__main__":
    asy.run(main())
