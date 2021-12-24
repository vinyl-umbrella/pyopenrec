from .config import HEADERS
import requests


def request(method: str, url: str, params=None, credentials=None) -> dict:
    """
    param
    -----
    method: HTTP method
    url: request URL
    params: dict
    credentials: dict
        uuid, access-token
    """
    header = HEADERS
    if credentials:
        header = {**header, **credentials}

    if method.upper() == "GET":
        res = requests.get(url, params=params, headers=header)
    elif method.upper() == "POST":
        res = requests.post(url, data=params, headers=header)
    elif method.upper() == "PUT":
        res = requests.put(url, data=params, headers=header)

    if res.status_code != 200:
        raise Exception("Failed to {}, {}\n\t{}".format(method, url, res.text))

    try:
        j = res.json()
        return {"status": res.status_code, "url": res.url, "data": j}
    except Exception as e:
        raise e
