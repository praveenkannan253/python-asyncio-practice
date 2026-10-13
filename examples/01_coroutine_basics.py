import asyncio


async def fetch_data(delay):
    print("Fetching data...")
    await asyncio.sleep(delay)  # Simulates an I/O wait
    print("Data fetched")
    return {"data": "Some data"}


async def main():
    print("Start of main coroutine")

    coro = fetch_data(2)  # Creates a coroutine object; doesn't run it yet
    print("Coroutine created, not started")

    result = await coro  # Runs the coroutine and waits for its result

    print(f"Received result: {result}")
    print("End of main coroutine")


asyncio.run(main())
