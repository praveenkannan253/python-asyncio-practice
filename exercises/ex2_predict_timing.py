# EXERCISE 2: Predict first, then run.
# Q1. What is the total time of Version A?  Q2. Version B?  Q3. Version C?
# Write your guesses in comments below BEFORE running.
# A = ?   B = ?   C = ?
import asyncio
import time


async def work(name, delay):
    await asyncio.sleep(delay)
    return name


async def version_a():
    await work("a1", 2)
    await work("a2", 3)


async def version_b():
    t1 = asyncio.create_task(work("b1", 2))
    t2 = asyncio.create_task(work("b2", 3))
    await t1
    await t2


async def version_c():
    t1 = asyncio.create_task(work("c1", 2))
    await t1
    t2 = asyncio.create_task(work("c2", 3))
    await t2


async def timed(fn):
    start = time.perf_counter()
    await fn()
    print(f"{fn.__name__}: {time.perf_counter() - start:.1f}s")


async def main():
    await timed(version_a)
    await timed(version_b)
    await timed(version_c)


asyncio.run(main())
