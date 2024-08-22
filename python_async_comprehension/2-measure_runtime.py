#!/usr/bin/env python3
# Measure runtime

import asyncio


async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    # Measure the runtime of async_comprehension executed 4 times in parallel
    start_time = asyncio.get_event_loop().time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end_time = asyncio.get_event_loop().time()
    return end_time - start_time

if __name__ == "__main__":
    print(asyncio.run(measure_runtime()))
