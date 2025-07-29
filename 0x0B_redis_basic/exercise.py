#!/usr/bin/env python3
"""
Cache class implementation with Redis backend
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """Cache class using Redis as backend"""

    def __init__(self):
        """Initialize Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
