from typing import Any

import requests

from .config import HEADERS


class Response:
    """
    status: HTTP status
    url: requested url
    data: return value
    """
    status: int
    url: str
    data: Any


def request(method: str, url: str, params=None, credentials=None, proxy=None) -> Response:
    """
    param
    -----
    method: HTTP method
    url: request URL
    params: dict
    credentials: dict
        uuid, access-token
    proxy: dict
        http, https
    """
    header = HEADERS
    if credentials:
        header = {**header, **credentials}

    if method.upper() == "GET":
        res = requests.get(url, params=params, headers=header, proxies=proxy)
    elif method.upper() == "POST":
        res = requests.post(url, data=params, headers=header, proxies=proxy)
    elif method.upper() == "PUT":
        res = requests.put(url, data=params, headers=header, proxies=proxy)
    elif method.upper() == "DELETE":
        return requests.delete(url, headers=header, proxies=proxy)

    if res.status_code != 200:
        raise Exception(f"Failed to {method}, {url}\n\t{res.text}")

    response = Response()
    try:
        response.status = res.status_code
        response.url = res.url
        j = res.json()

        if "message" in j:
            raise Exception(j["message"])

        if "data" in j and "items" in j["data"]:
            items = j["data"]["items"]
            if list(j["data"].keys()) == ['type', 'items'] and isinstance(items, list):
                response.data = items
            else:
                response.data = j["data"]
        else:
            response.data = j
        return response

    except Exception as e:
        raise e
