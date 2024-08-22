#!/usr/bin/env python3
# Async generator

import asyncio
import random


async def async_generator():
    # This function will return 10 random numbers between 0 and 10
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
