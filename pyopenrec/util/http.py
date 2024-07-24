from typing import Optional, Union

import requests

from ..credentials import OpenrecCredentials
from . import const, exceptions


def get(
    url: str,
    param: Optional[dict] = {},
    credentials: Optional[OpenrecCredentials] = None,
) -> Union[dict, list]:
    """
    Get request to url
    Args:
        url: url to get
        param: parameters
        credentials: login credentials
    Returns:
        dict: json response
    """
    headers = const.HEADERS
    if credentials:
        headers = {**const.HEADERS, **credentials.params}
    res = requests.get(url, headers=headers, params=param)
    try:
        j = res.json()
    except:
        raise exceptions.PyopenrecException(f"Invalid json response from {url}: {res.status_code}")

    if res.ok:
        return j
    else:
        raise exceptions.PyopenrecException(f"Error {res.status_code}: {j.get('message')}")


def post(
    url: str,
    data: Optional[dict] = {},
    credentials: Optional[OpenrecCredentials] = None,
) -> Union[dict, list]:
    """
    Post request to url
    Args:
        url: url to post
        data: data to post
        credentials: login credentials
    Returns:
        dict: json response
    """
    headers = const.HEADERS
    if credentials:
        headers = {**const.HEADERS, **credentials.params}
    res = requests.post(url, headers=headers, data=data)
    try:
        j = res.json()
    except:
        raise exceptions.PyopenrecException(f"Invalid json response from {url}: {res.status_code}")

    if res.ok and j.get("status") == 0:
        return j
    else:
        print(j)
        raise exceptions.PyopenrecException(f"Error {res.status_code}: {j.get('message')}")


def put(
    url: str,
    data: Optional[dict] = {},
    credentials: Optional[OpenrecCredentials] = None,
) -> Union[dict, list]:
    """
    Put request to url
    Args:
        url: url to put
        data: data to put
        credentials: login credentials
    Returns:
        dict: json response
    """
    headers = const.HEADERS
    if credentials:
        headers = {**const.HEADERS, **credentials.params}
    res = requests.put(url, headers=headers, data=data)
    try:
        j = res.json()
    except:
        raise exceptions.PyopenrecException(f"Invalid json response from {url}: {res.status_code}")

    if res.ok:
        return j
    else:
        raise exceptions.PyopenrecException(f"Error {res.status_code}: {j.get('message')}")


def delete(
    url: str,
    credentials: Optional[OpenrecCredentials] = None,
) -> Union[dict, list]:
    """
    Delete request to url
    Args:
        url: url to delete
        credentials: login credentials
    Returns:
        dict: json response
    """
    headers = const.HEADERS
    if credentials:
        headers = {**const.HEADERS, **credentials.params}
    res = requests.delete(url, headers=headers)
    try:
        j = res.json()
    except:
        raise exceptions.PyopenrecException(f"Invalid json response from {url}: {res.status_code}")

    if res.ok:
        return j
    else:
        raise exceptions.PyopenrecException(f"Error {res.status_code}: {j.get('message')}")
