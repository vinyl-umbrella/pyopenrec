from ..config import HEADERS
import requests


def get(url: str, params=None, credentials=None) -> dict:
    header = HEADERS
    if credentials:
        header = {header, credentials}

    res = requests.get(url, params=params, headers=header)
    # print(res.url)
    if res.status_code != 200:
        return {"status": res.status_code}
    return {"status": res.status_code, "data": res.json()}


def post(url: str, params=None, credentials=None) -> dict:
    header = HEADERS
    if credentials:
        header = {header, credentials}

    res = requests.post(url, params=params, headers=header)
    if res.status_code != 200:
        return {"status": res.status_code}
    return {"status": res.status_code, "data": res.json()}
