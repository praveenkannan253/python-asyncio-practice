# EXERCISE 1: Fix the bug.
# Running this prints a "coroutine ... was never awaited" warning.
# Goal: make it print "Hello from greet" and return the message.
import asyncio


async def greet():
    await asyncio.sleep(1)
    return "Hello from greet"


async def main():
    message = greet()  # TODO: fix this line
    print(message)


asyncio.run(main())
