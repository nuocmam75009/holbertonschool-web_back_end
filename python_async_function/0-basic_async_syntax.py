#!/usr/bin/env python3

# Task 0

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    # Async with 1 arg
    random_delay = random.uniform(0, max_delay)
    await asyncio.sleep(random_delay)
    return (random_delay)
