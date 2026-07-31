import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException

from api.security import make_api_key_dependency
from guardian.config import GuardianConfig


class TestApiKeyDependency(unittest.TestCase):
    def test_disabled_when_no_key_configured(self):
        config = GuardianConfig(api_key=None)
        require_api_key = make_api_key_dependency(config)
        # Should not raise, regardless of header
        require_api_key(authorization=None)
        require_api_key(authorization="Bearer anything")

    def test_missing_header_rejected_when_key_configured(self):
        config = GuardianConfig(api_key="secret123")
        require_api_key = make_api_key_dependency(config)
        with self.assertRaises(HTTPException) as ctx:
            require_api_key(authorization=None)
        self.assertEqual(ctx.exception.status_code, 401)

    def test_wrong_key_rejected(self):
        config = GuardianConfig(api_key="secret123")
        require_api_key = make_api_key_dependency(config)
        with self.assertRaises(HTTPException) as ctx:
            require_api_key(authorization="Bearer wrong")
        self.assertEqual(ctx.exception.status_code, 401)

    def test_correct_key_accepted(self):
        config = GuardianConfig(api_key="secret123")
        require_api_key = make_api_key_dependency(config)
        require_api_key(authorization="Bearer secret123")  # should not raise

    def test_malformed_header_rejected(self):
        config = GuardianConfig(api_key="secret123")
        require_api_key = make_api_key_dependency(config)
        with self.assertRaises(HTTPException):
            require_api_key(authorization="secret123")  # missing "Bearer " prefix


if __name__ == "__main__":
    unittest.main()
