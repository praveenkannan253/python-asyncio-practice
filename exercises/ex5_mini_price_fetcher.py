# EXERCISE 5 (mini project): Async price fetcher.
# Simulate fetching prices for several stock symbols.
# Requirements:
#   1. fetch_price(symbol) sleeps 1-2 seconds, returns (symbol, price)
#   2. Fetch 6 symbols concurrently using TaskGroup
#   3. Print a sorted table (highest price first) and the total time
#   4. Bonus: make one symbol fail randomly and handle it without crashing
import asyncio
import random
import time

SYMBOLS = ["TCS", "INFY", "RELIANCE", "HDFCBANK", "ITC", "WIPRO"]


async def fetch_price(symbol):
    # TODO
    ...


async def main():
    # TODO
    ...


asyncio.run(main())
