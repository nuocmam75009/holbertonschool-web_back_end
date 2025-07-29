#!/usr/bin/env python3
"""
Cache class implementation with Redis backend
"""
import redis
import uuid
from typing import Union


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
