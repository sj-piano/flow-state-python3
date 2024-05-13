import unittest
from unittest.mock import Mock

from flow_state.service.user_service import UserService

users = 'user1 user2 user3 user4'.split()
uncached_users = 'user3 user4'.split()


class TestUserService(unittest.TestCase):
    def setUp(cls):
        cls.user_service = UserService()
        # Replace the actual cache service with a Mock object
        cls.user_service.cache_service = Mock()

    def test_fetch_user_info(self):
        self.user_service._fetch_user_info('user1')
        self.user_service.cache_service.retrieve.assert_not_called()

    def test_save_user_info(self):
        info_str = '{"id": "1", "name": "User1"}'
        self.user_service.save_user_info('user1', info_str)
        self.user_service.cache_service.save.assert_called_once()

    def test_get_user_info(self):
        self.user_service.get_user_info('user1', uncached_users)
        self.user_service.cache_service.retrieve.assert_called_once()

    def test_get_user_info_uncached(self):
        self.user_service.get_user_info('user3', uncached_users)
        self.user_service.cache_service.retrieve.assert_not_called()
