#!/usr/bin/env python3

# Task 7

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    # Return a tuple with the first element as the string and the
    # second element as the square of the number
    return (k, v ** 2)
