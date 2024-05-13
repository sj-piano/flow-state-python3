import json
import unittest
from unittest.mock import MagicMock, patch

from flow_state.service.cache_service import CacheService

# setup
redis_class_path = 'flow_state.service.cache_service.redis.StrictRedis'


class TestCacheService(unittest.TestCase):
    @patch(redis_class_path)
    def setUp(self, mock_redis):
        self.cache_service = CacheService()
        self.mock_redis = mock_redis.return_value

    def test_save_calls_setex(self):
        value = 'test_value'
        value_str = json.dumps(value)
        self.cache_service.save('test_key', value)
        default_lifetime = 30
        self.mock_redis.setex.assert_called_once_with('test_key', default_lifetime, value_str)

    def test_retrieve_calls_get(self):
        self.mock_redis.get.return_value = json.dumps('test_value')
        self.cache_service.retrieve('test_key')
        self.mock_redis.get.assert_called_once_with('test_key')

    def test_save_with_disabled_cache_does_not_call_setex(self):
        self.cache_service.cache_enabled = False
        with self.assertRaises(RuntimeError):
            self.cache_service.save('test_key', 'test_value')
        self.mock_redis.setex.assert_not_called()

    def test_retrieve_with_disabled_cache_does_not_call_get(self):
        self.cache_service.cache_enabled = False
        with self.assertRaises(RuntimeError):
            self.cache_service.retrieve('test_key')
        self.mock_redis.get.assert_not_called()
