import hashlib
import inspect
import json
from functools import wraps

import redis

from ..config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

use_ssl = False


class CacheService:
    """A class to interact with a Redis cache."""

    def __init__(self, cache_enabled: str = 'true'):
        self.host: str = REDIS_HOST
        self.port: int = REDIS_PORT
        self.password: str = REDIS_PASSWORD
        self.client = redis.StrictRedis(
            host=self.host,
            port=self.port,
            db=0,
            password=self.password,
            ssl=use_ssl,
            socket_timeout=1,
            socket_connect_timeout=1,
        )
        self.cache_enabled = True if cache_enabled.lower() == 'true' else False

    def save(self, key: str, value, lifetime: int = 30) -> None:
        """
        Save the provided value in the cache under the given key with a specified lifetime.

        Parameters:
        key (str): The unique identifier for the cached value.
        value (str): The data to be cached. We expect this to be a JSON serializable object.
        lifetime (int): The time duration in seconds for which the value will be stored in the cache.
        """
        if not self.cache_enabled:
            raise RuntimeError('Cache is not enabled.')
        value_str = json.dumps(value)
        self.client.setex(key, lifetime, value_str)

    def retrieve(self, key: str) -> dict | None:
        # Retrieve the value from the cache.
        # We deserialize the value from JSON before returning it.
        if not self.cache_enabled:
            raise RuntimeError('Cache is not enabled.')
        if (value_str := self.client.get(key)) is not None:
            value = json.loads(value_str)
            return value
        return None


def cache_decorator_for_async_instance_method(lifetime: int):
    # A decorator designed to add caching to async instance methods of a class.
    # Slugs are checked against the uncached_slugs attribute of the calling instance.
    # - If the slug is listed there, the function is called without caching.

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # print(f"Function {func.__name__} called with args={args}, kwargs={kwargs}")
            # Confirm that the function is async.
            if not inspect.iscoroutinefunction(func):
                raise TypeError('This decorator is only to be used with async functions.')
            # See if the calling instance has a cache service that is enabled.
            cache_service = getattr(self, 'cache_service', None)
            if not cache_service or not cache_service.cache_enabled:
                return await func(self, *args, **kwargs)
            # Get the slug from the keyword args.
            try:
                slug = kwargs['slug']
            except KeyError as e:
                raise KeyError("Missing keyword argument: 'slug'.") from e
            # Check if this slug is in the calling instance's uncached list.
            uncached_slugs = getattr(self, 'uncached_slugs', [])
            if uncached_slugs:
                if slug in uncached_slugs:
                    return await func(*args, **kwargs)
            # Generate a cache key based on the function name and arguments.
            input_bytes = f'{func.__name__}_{args}_{kwargs}'.encode('utf-8')
            # rocket22_get_dashboard
            cache_key = f'{slug}_{func.__name__}:' + hashlib.sha256(input_bytes).hexdigest()
            print(f'cache_key = {cache_key}')
            # Retrieve from cache. If found, return the result.
            if result := cache_service.retrieve(cache_key) is not None:
                return result
            # Call the function, cache the result, and return the result.
            result = await func(*args, **kwargs)
            result_str = result.model_dump_json()
            cache_service.save(key=cache_key, value=result_str, lifetime=lifetime)
            return result

        return wrapper

    return decorator
