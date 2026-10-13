import asyncio
import time


async def fetch_data(id, delay):
    print(f"Fetching data for id {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id {id}")
    return {"id": id, "data": f"Sample data from coroutine {id}"}


async def main():
    start = time.perf_counter()
    task1 = asyncio.create_task(fetch_data(1, 2))
    task2 = asyncio.create_task(fetch_data(2, 3))
    task3 = asyncio.create_task(fetch_data(3, 1))

    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(result1, result2, result3)
    print(f"Total: {time.perf_counter() - start:.1f}s (expected ~3s)")


asyncio.run(main())
