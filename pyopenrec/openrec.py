import requests
from .util import http
from .capture import Capture
from .channel import Channel
from .chat import Chat
from .comment import Comment
from .playlist import Playlist
from .video import Video
from .yell import Yell
from .util.config import HEADERS, AUTHORIZED_API


class Openrec(Capture, Channel, Chat, Comment, Playlist, Video, Yell):
    """
    # OPENREC.tv api client.

    If you don't give email and password, you will get credentials of non-login-user.
    Non-login-user can post capture rection, but cannot post comment, get own user info and update chat config.

    param
    -----
    email: str
        YOUR EMAIL
    password: str
        YOUR PASSWORD
    proxy: dict
        {
            "http": "",
            "https": ""
        }
    """

    is_login = False
    id = ""
    name = ""
    _credentials = {}

    def __init__(self, email=None, password=None, proxy=None):
        with requests.session() as s:
            r = s.post("https://www.openrec.tv/api-tv/user",
                       headers=HEADERS)
            if r.status_code != 200:
                raise Exception("Failed to get initial param.", r.text)

            self._credentials["uuid"] = r.cookies["uuid"]
            self._credentials["token"] = r.cookies["token"]
            self._credentials["random"] = r.cookies["random"]

            if email is not None and password is not None:
                param = {"mail": email, "password": password}
                cookie = {"AWSELB": "", "AWSELBCORS": "", **self._credentials}

                r = s.post("https://www.openrec.tv/viewapp/v4/mobile/user/login",
                           data=param, headers=HEADERS, cookies=cookie)
                if r.status_code != 200:
                    raise Exception("Failed to login.", r.text)

                # self._credentials["sessid"] = r.cookies["PHPSESSID"]
                self._credentials["access-token"] = r.cookies["access_token"]
                self._credentials["uuid"] = r.cookies["uuid"]
                self._credentials["token"] = r.cookies["token"]
                self._credentials["random"] = r.cookies["random"]
                self.is_login = True

        self.me()

    def me(self) -> dict:
        """
        Get login user info.
        """
        if self.is_login:
            url = AUTHORIZED_API + "/users/me"

            info = http.request("GET", url, credentials=self._credentials)
            if info["status"] != 200:
                raise Exception(info)

            self.id = info["data"]["data"]["items"][0]["id"]
            self.name = info["data"]["data"]["items"][0]["nickname"]
        else:
            header = {**HEADERS, **self._credentials}
            r = requests.get("https://www.openrec.tv/api-tv/user",
                             headers=header, cookies=self._credentials)
            j = r.json()
            self.name = j["name"]
