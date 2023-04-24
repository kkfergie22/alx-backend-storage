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
cache: Dict[str, Dict[str, Union[str, int]]]
A dictionary that stores cached results and access counts.

"""

import requests
import time

CACHE_EXPIRATION_TIME = 10
cache = {}


def cache_decorator(func):
    """
    A decorator that adds caching behavior to a function.
    Args:
    func: A function that returns a string.

    Returns:
       A wrapper function that adds caching behavior to the original function.
    """
    def wrapper(url):
        """
    A wrapper function that adds caching behavior to the original function.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content of the specified URL, either from the cache or by
        fetching it using requests.get.
    """
        if url in cache and cache[url]["expires"] > time.time():
            # Use cached result if available and not expired
            cache[url]["count"] += 1
            return cache[url]["content"]
        else:
            # Fetch new result and cache it
            content = func(url)
            cache[url] = {
                "content": content,
                "count": 1,
                "expires": time.time() + CACHE_EXPIRATION_TIME
            }
            return content
    return wrapper


@cache_decorator
def get_page(url):
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
