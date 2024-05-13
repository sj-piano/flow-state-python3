import json
from functools import wraps

from .cache_service import CacheService, cache_decorator_for_async_instance_method


def extract_slug_from_user_session(slug_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, user_session, *args, **kwargs):
            # Dynamically extract the specified attribute from user_session and add it to the kwargs.
            slug_value = getattr(user_session, slug_name)
            kwargs['slug'] = slug_value
            return await func(self, user_session, *args, **kwargs)

        return wrapper

    return decorator


def caching_with_slug_extraction(slug_name, lifetime):
    def combined_decorator(func):
        cached_func = cache_decorator_for_async_instance_method(lifetime)(func)
        return extract_slug_from_user_session(slug_name)(cached_func)

    return combined_decorator


def test_decorator(func):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, user_session, *args, **kwargs):
            print(f'test_decorator: {kwargs}')
            return await func(self, user_session, *args, **kwargs)

        return wrapper


class UserService:
    """Service class for user-related operations."""

    def __init__(self, uncached_users: list[str]):
        self.cache_service = CacheService()
        self.uncached_slugs = uncached_users

    def _fetch_user_info(self, username: str) -> dict:
        """
        Fetch user information.

        Typically, we would fetch this information from a database or an external service.

        For the purpose of this example, we will generate some dummy data from the username.
        """
        info = {
            'id': username.replace('user', ''),
            'name': username.capitalize(),
        }
        return info

    def cache_user_info(self, username: str, info: dict) -> None:
        """
        Save user information to the cache.

        Parameters:
        username (str): The unique identifier for the user.
        """
        self.cache_service.save(username, info)

    def get_user_info(self, username: str, uncached_users: list[str]) -> dict:
        """
        Retrieve user information from the cache if it exists, otherwise fetch the information and cache it.

        Parameters:
        username (str): The unique identifier for the user.

        Returns:
        dict: The user information.
        """
        if username in uncached_users:
            return self._fetch_user_info(username)
        if (info := self.cache_service.retrieve(username)) is not None:
            return info
        info = self._fetch_user_info(username)
        self.cache_user_info(username, uncached_users, info)
        return info

    @caching_with_slug_extraction(slug_name='username', lifetime=300)
    async def get_user_info_2(self, user_session) -> dict:
        info = self._fetch_user_info(user_session.username)
        return info
