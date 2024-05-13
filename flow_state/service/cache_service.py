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

    def save(self, key: str, value: str, lifetime: int = 30) -> None:
        """
        Save the provided value in the cache under the given key with a specified lifetime.

        Parameters:
        key (str): The unique identifier for the cached value.
        value (str): The data to be cached. This should be in a format suitable for caching.
        lifetime (int): The time duration in seconds for which the value will be stored in the cache.
        """
        if not self.cache_enabled:
            raise RuntimeError('Cache is not enabled.')
        self.client.setex(key, lifetime, value)

    def retrieve(self, key: str) -> dict | None:
        if not self.cache_enabled:
            raise RuntimeError('Cache is not enabled.')
        if (value := self.client.get(key)) is not None:
            return value
        return None
