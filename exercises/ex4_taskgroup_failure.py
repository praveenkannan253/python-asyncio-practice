# EXERCISE 4: Observe error handling. Requires Python 3.11+.
# Task 2 raises an error after 1 second.
# Part A: run with TaskGroup. Does task 3 finish? (Write your observation below.)
# Part B: rewrite using asyncio.gather. Does task 3 still finish?
# Observation A: ?
# Observation B: ?
import asyncio


async def job(id, delay, fail=False):
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(f"job {id} failed")
    print(f"job {id} finished")
    return id


async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(job(1, 2))
            tg.create_task(job(2, 1, fail=True))
            tg.create_task(job(3, 3))
    except* ValueError as eg:
        print("Caught:", eg.exceptions)


asyncio.run(main())
