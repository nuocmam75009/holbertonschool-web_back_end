#!/usr/bin/env python3

# Task 1

import asyncio
import random
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    # Async with 2 args
    list = []
    for i in range(n):
        list.append(await wait_random(max_delay))
    return sorted(list)
