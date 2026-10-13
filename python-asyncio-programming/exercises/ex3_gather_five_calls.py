# EXERCISE 3: Run 5 simulated API calls concurrently with asyncio.gather.
# Delays are random between 1 and 3 seconds.
# Goal: total time should be about the longest delay, not the sum.
# Print the results in the same order as the ids.
import asyncio
import random
import time


async def call_api(id):
    delay = random.uniform(1, 3)
    await asyncio.sleep(delay)
    return f"response-{id} ({delay:.1f}s)"


async def main():
    start = time.perf_counter()
    # TODO: use asyncio.gather to call_api for ids 1..5
    results = []
    for r in results:
        print(r)
    print(f"Total: {time.perf_counter() - start:.1f}s")


asyncio.run(main())
