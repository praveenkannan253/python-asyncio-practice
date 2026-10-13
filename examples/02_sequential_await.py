import asyncio
import time


async def fetch_data(id, delay):
    print(f"Fetching data for id {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id {id}")
    return {"id": id}


async def main():
    start = time.perf_counter()
    result1 = await fetch_data(1, 2)
    result2 = await fetch_data(2, 2)
    print(result1, result2)
    print(f"Total: {time.perf_counter() - start:.1f}s (expected ~4s, no benefit)")


asyncio.run(main())
