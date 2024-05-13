import json

from .cache_service import CacheService


class UserService:
    """Service class for user-related operations."""

    def __init__(self):
        self.cache_service = CacheService()

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
        info_str = json.dumps(info)
        return info_str

    def save_user_info(self, username: str, info_str: str) -> None:
        """
        Save user information to the cache.

        Parameters:
        username (str): The unique identifier for the user.
        """
        self.cache_service.save(username, info_str)

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
        info_str = self._fetch_user_info(username)
        self.save_user_info(username, uncached_users, info_str)
        return json.loads(info_str)
