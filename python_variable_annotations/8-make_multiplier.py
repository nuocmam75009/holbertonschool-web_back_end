#!/usr/bin/env python3

# Task 8

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    # Return a function that multiplies a number by the multiplier
    def multiply(n: float) -> float:
        return n * multiplier
    return multiply
