import requests


def add_auth_headers(headers: dict, token: str):
    headers['Authorization'] = f'Key {token}'


class DeskAuthorizationError(Exception):
    pass


class DeskClient:

    BASE_URL_PROD = 'https://api-cluster.postcenter.io'

    def __init__(self, api_token=None, base_url=None):
        self.api_token = api_token
        if base_url is None:
            self.base_url = self.BASE_URL_PROD

    def __check_response_errors(self, response):
        if response.status_code == 401:
            raise DeskAuthorizationError()

    def __desk_request(
            self, method: str, path: str,
            params: dict = None, headers: dict = None
    ):
        if headers is None:
            headers = {}
        add_auth_headers(headers, self.api_token)

        url = f'{self.base_url}/{path}/'
        response = requests.request(method, url, params=params, headers=headers)
        self.__check_response_errors(response)
        return response

    def __get_request(
            self, path: str, params: dict = None, headers: dict = None
    ):
        return self.__desk_request('get', path, params, headers)

    def ping(self):
        response = self.__get_request('v2/ping')
        return response.json()['message']