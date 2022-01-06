from .config import HEADERS
import requests


def request(method: str, url: str, params=None, credentials=None, proxy=None) -> dict:
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

    if res.status_code != 200:
        raise Exception(f"Failed to {method}, {url}\n\t{res.text}")

    try:
        j = res.json()
        return {"status": res.status_code, "url": res.url, "data": j}
    except Exception as e:
        raise e
