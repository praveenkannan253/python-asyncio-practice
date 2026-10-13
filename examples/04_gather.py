import asyncio
import time


async def fetch_data(id, delay):
    print(f"Fetching data for id {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id {id}")
    return {"id": id, "data": f"Sample data from coroutine {id}"}


async def main():
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 1),
        fetch_data(3, 3),
    )
    for result in results:  # same order as the arguments
        print(f"Received result: {result}")
    print(f"Total: {time.perf_counter() - start:.1f}s (expected ~3s)")


asyncio.run(main())
