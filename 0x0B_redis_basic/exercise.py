#!/usr/bin/env python3
"""
Cache class implementation with Redis backend
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count method calls using Redis INCR

    Args:
        method: The method to be decorated

    Returns:
        Callable: The wrapped method that counts calls
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments call count and calls original method"""
        # Use the qualified name as the key
        key = method.__qualname__
        # Increment the count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store input and output history using Redis lists

    Args:
        method: The method to be decorated

    Returns:
        Callable: The wrapped method that stores history
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that stores input/output history and calls original method"""
        # Create input and output list keys using qualified name
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store input arguments as string
        self._redis.rpush(input_key, str(args))

        # Execute the original method to get output
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, str(output))

        # Return the original output
        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls for a particular function

    Args:
        method: The method to replay history for
    """
    # Get the cache instance from the method
    cache = method.__self__

    # Get the qualified name for the method
    qualname = method.__qualname__

    # Get the call count
    call_count = cache._redis.get(qualname)
    if call_count is None:
        call_count = 0
    else:
        call_count = int(call_count)

    # Get input and output lists
    input_key = f"{qualname}:inputs"
    output_key = f"{qualname}:outputs"

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    # Display the header
    print(f"{qualname} was called {call_count} times:")

    # Loop over inputs and outputs using zip
    for input_data, output_data in zip(inputs, outputs):
        # Decode bytes to string
        input_str = input_data.decode('utf-8')
        output_str = output_data.decode('utf-8')

        # Format the output
        print(f"{qualname}(*{input_str}) -> {output_str}")


class Cache:
    """Cache class using Redis as backend"""

    def __init__(self):
        """Initialize Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key

        Args:
            data: Data to store (str, bytes, int, or float)

        Returns:
            str: The random key used to store the data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieve data from Redis with optional conversion function

        Args:
            key: The key to retrieve data for
            fn: Optional callable to convert the data

        Returns:
            The retrieved data, optionally converted by fn
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis and convert to string

        Args:
            key: The key to retrieve data for

        Returns:
            The retrieved data as string, or None if key doesn't exist
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis and convert to integer

        Args:
            key: The key to retrieve data for

        Returns:
            The retrieved data as integer, or None if key doesn't exist
        """
        return self.get(key, int)
