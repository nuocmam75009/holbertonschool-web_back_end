#!/usr/bin/env python3

# Task 9

from typing import List, Tuple, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    #  Return a list of tuples with the first element as the string and the
    #  second element as the length of the string
    return [(i, len(i)) for i in lst]
