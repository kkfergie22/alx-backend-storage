#!/usr/bin/env python3

"""
Web module for implementing an expiring web cache and tracker.

This module defines a get_page function that uses the requests module to obtain
the HTML content of a particular URL and caches the result with an expiration
time of 10 seconds. The number of times a URL is accessed is also tracked.

Functions:
    get_page(url: str) -> str:
        Returns the HTML content of the specified URL, either from the cache or
        by fetching it using requests.get.

Decorators:
    cache_decorator(func: Callable[..., str]) -> Callable[..., str]:
        A decorator that adds caching behavior to a function.

Variables:
    CACHE_EXPIRATION_TIME: int
        The number of seconds until a cached result expires.
"""

import requests
import redis
import time
from typing import Callable

redis_client = redis.Redis(host='localhost', port=6379, db=0)
CACHE_EXPIRATION_TIME: int = 10


def cache_decorator(func: Callable[..., str]) -> Callable[..., str]:
    """
    A decorator that adds caching behavior to a function.

    Args:
        func: A function that returns a string.

    Returns:
        A wrapper function that adds caching behavior to the original function.
    """
    def wrapper(url: str) -> str:
        """
        A wrapper function that adds caching behavior to the original function.

        Args:
            url: The URL to fetch.

        Returns:
            The HTML content of the specified URL, either from the cache or by
            fetching it using requests.get.
        """
        cached_content = redis_client.get(url)
        if cached_content is not None:
            redis_client.incr(f"count:{url}")
            return cached_content.decode('utf-8')
        else:
            content = func(url)
            redis_client.set(url, content, ex=CACHE_EXPIRATION_TIME)
            redis_client.set(f"count:{url}", 1, ex=CACHE_EXPIRATION_TIME)
            return content

    return wrapper


@cache_decorator
def get_page(url: str) -> str:
    """
    Returns the HTML content of the specified URL, either from the cache or by
    fetching it using requests.get.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content of the specified URL, either from the cache or by
        fetching it using requests.get.
    """
    response = requests.get(url)
    content = response.content.decode('utf-8')
    return content
