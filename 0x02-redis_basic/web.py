#!/usr/bin/env python3

import redis
import time
import requests
from typing import Optional


class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0, expire_time=10):
        self.expire_time = expire_time
        self.redis = redis.Redis(host=host, port=port, db=db)

    def get(self, key):
        value = self.redis.get(key)
        if value is not None:
            return value.decode('utf-8')
        return None

    def set(self, key, value):
        self.redis.setex(key, self.expire_time, value)

    def delete(self, key):
        self.redis.delete(key)


cache = RedisCache()


def cache_decorator(func):
    def wrapper(url: str) -> Optional[str]:
        content = cache.get(url)
        if content is not None:
            # Use cached result if available
            cache.redis.incr(f"count:{url}")
            return content

        # Fetch new result and cache it
        response = requests.get(url)
        content = response.content.decode('utf-8')
        cache.set(url, content)
        cache.redis.setex(f"count:{url}", cache.expire_time, 1)
        return content

    return wrapper


@cache_decorator
def get_page(url: str) -> Optional[str]:
    return requests.get(url).text
