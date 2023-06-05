from enum import Enum
from typing import List, Dict, Optional

import requests


class DeskAuthorizationError(Exception):
    pass


def add_auth_headers(headers: dict, token: str):
    headers["Authorization"] = f"Key {token}"


def check_response_errors(response):
    if response.status_code == 401:
        raise DeskAuthorizationError()


class DeskEntityType(str, Enum):
    client = "client"
    ticket = "ticket"


class DeskClient:

    BASE_URL_PROD = "https://api-cluster.postcenter.io"

    def __init__(self, api_token=None, base_url=None):
        """
        :param api_token: Desk's API Token
        :param base_url: Desk's API environment base URL
        """
        self.api_token = api_token
        if base_url is None:
            self.base_url = self.BASE_URL_PROD
        else:
            self.base_url = base_url

    def __desk_request(
        self,
        method: str,
        path: str,
        params: dict = None,
        body: dict = None,
        headers: dict = None,
    ):
        if headers is None:
            headers = {}
        add_auth_headers(headers, self.api_token)

        url = f"{self.base_url}/{path}/"
        response = requests.request(
            method, url, json=body, params=params, headers=headers, timeout=30
        )
        check_response_errors(response)
        return response

    def __get_request(self, path: str, params: dict = None, headers: dict = None):
        return self.__desk_request("get", path, params, headers=headers)

    def __post_request(
        self, path: str, body: dict, params: dict = None, headers: dict = None
    ):
        return self.__desk_request("post", path, params, body, headers)

    def __put_request(
        self, path: str, body: dict, params: dict = None, headers: dict = None
    ):
        return self.__desk_request("put", path, params, body, headers)

    def ping(self):
        response = self.__get_request("v2/ping")
        return response.json()["message"]

    def accounts(self):
        response = self.__get_request("v2/accounts/all")
        return response.json()["accounts"]

    def agents(self):
        response = self.__get_request("v2/agents")
        return response.json()["agents"]

    def send_hsm(
        self,
        sender: str,
        recipient: str,
        template: str,
        parameters: List[str],
        close_ticket: bool = False,
        header: dict = None,
    ):
        response = self.__post_request(
            "v2/message/hsm",
            {
                "account": sender,
                "phone": recipient,
                "name": template,
                "parameters": parameters,
                "close_ticket": close_ticket,
                "header": header,
            },
        )
        return response.json()

    def send_hsm_v2(
        self,
        sender: str,
        recipient: str,
        template: str,
        parameters: List[str],
        campaign_id: Optional[str] = None,
        entry_id: Optional[str] = None,
        close_ticket: bool = False,
        header: dict = None,
    ):
        if campaign_id and entry_id:
            response = self.__post_request(
                "v2/message/hsm",
                {
                    "account": sender,
                    "phone": recipient,
                    "name": template,
                    "parameters": parameters,
                    "campaign_id": campaign_id,
                    "entry_id": entry_id,
                    "close_ticket": close_ticket,
                    "header": header,
                },
            )
        else:
            response = self.__post_request(
                "v2/message/hsm",
                {
                    "account": sender,
                    "phone": recipient,
                    "name": template,
                    "parameters": parameters,
                    "close_ticket": close_ticket,
                    "header": header,
                },
            )
        return response

    def put_metadata(
        self, entity: DeskEntityType, entity_id: str, metadata: Dict[str, str]
    ):
        response = self.__put_request(f"v2/metadata/{entity}/{entity_id}", metadata)
        return response.json()

    def get_ticket(self, ticket_id: str):
        response = self.__get_request(f"v2/ticket/{ticket_id}")
        return response.json()
