# Requires Python 3.11+
import asyncio
import time


async def fetch_data(id, delay):
    print(f"Fetching data for id {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id {id}")
    return {"id": id, "data": f"Sample data from coroutine {id}"}


async def main():
    start = time.perf_counter()
    tasks = []

    async with asyncio.TaskGroup() as tg:
        for i, delay in enumerate([2, 1, 3], start=1):
            tasks.append(tg.create_task(fetch_data(i, delay)))

    # All tasks are finished here
    for task in tasks:
        print(f"Received result: {task.result()}")
    print(f"Total: {time.perf_counter() - start:.1f}s (expected ~3s)")


asyncio.run(main())
