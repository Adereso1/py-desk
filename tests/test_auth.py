import unittest
from unittest.mock import patch, MagicMock

from pydesk import DeskClient
from pydesk.desk_client import DeskAuthorizationError


class AuthTestCase(unittest.TestCase):

    TEST_TOKEN = 'test_token'

    PING_SUCCESS_RESPONSE = {'message': 'Pong!'}

    @patch('requests.request')
    def test_auth(self, request_mock):
        response_mock = MagicMock()
        request_mock.return_value = response_mock
        response_mock.json.return_value = self.PING_SUCCESS_RESPONSE

        client = DeskClient(self.TEST_TOKEN)
        response_mock.status_code = 401
        self.assertRaises(DeskAuthorizationError, lambda: client.ping())

        response_mock.status_code = 200
        response = client.ping()
        self.assertEqual(self.PING_SUCCESS_RESPONSE['message'], response)
