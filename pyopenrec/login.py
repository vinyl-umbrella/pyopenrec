import requests
from .config import HEADERS


def login(email=None, password=None) -> dict:
    """
    param
    -----
    email: str
        YOUR EMAIL
    password: str
        YOUR PASSWORD

    return
    ------
    {
        status: HTTP status code,
        data: {}
    }


    If you don't give email and password, you will get credentials of non-login-user.
    Non-login-user can post capture rection, but cannot post comment, see own user info and update chat config.
    """
    credentials = {}
    if email is not None and password is not None:
        with requests.Session() as s:
            r = s.post("https://www.openrec.tv/api-tv/user",
                       headers=HEADERS)
            if r.status_code != 200:
                return {"status": r.status_code, "data": r.json()}

            param = {
                "mail": email,
                "password": password
            }
            cookie = {
                "Uuid": r.cookies["uuid"],
                "Token": r.cookies["token"],
                "Random": r.cookies["random"],
                "_gcl_au": "",
                "AWSELB": "",
                "AWSELBCORS": ""
            }

            r = s.post("https://www.openrec.tv/viewapp/v4/mobile/user/login",
                       data=param, headers=HEADERS, cookies=cookie)
            if r.status_code != 200:
                return {"status": r.status_code, "data": r.json()}

            credentials["uuid"] = r.cookies["uuid"]
            credentials["token"] = r.cookies["token"]
            credentials["random"] = r.cookies["random"]
            # credentials["ssid"] = r.cookies["PHPSESSID"]
            credentials["access_token"] = r.cookies["access_token"]

    else:
        with requests.Session() as s:
            r = s.post("https://www.openrec.tv/api-tv/user")
            if r.status_code != 200:
                return {"status": r.status_code, "data": r.json()}

            credentials["uuid"] = r.cookies["uuid"]
            credentials["token"] = r.cookies["token"]
            credentials["random"] = r.cookies["random"]

    return {"status": 200, "data": credentials}
