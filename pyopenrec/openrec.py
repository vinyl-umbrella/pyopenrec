import requests

from .capture import Capture
from .channel import Channel
from .chat import Chat
from .comment import Comment
from .playlist import Playlist
from .util import http
from .util.config import AUTHORIZED_API, HEADERS
from .video import Video
from .yell import Yell


class Openrec(Capture, Channel, Chat, Comment, Playlist, Video, Yell):
    """
    # OPENREC.tv api client.

    If you don't give email and password, you will get credentials of non-login-user.
    Non-login-user can post capture rection, but cannot post comment, get own user info and update chat config.

    If you use OAuth, you cannot login with this function. You need to set credentials (uuid, token, random, access-token)

    param
    -----
    email: str
        YOUR EMAIL
    password: str
        YOUR PASSWORD
    credentials: dict
        {
            "uuid": "",
            "token": "",
            "random": "",
            "access-token": ""
        }
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
    _proxy = {}

    def __init__(self, email=None, password=None, credentials=None, proxy=None):
        self._proxy = proxy
        if credentials:
            self._credentials = credentials
            self.is_login = True
        else:
            with requests.session() as s:
                r = s.post("https://www.openrec.tv/api-tv/user",
                           headers=HEADERS, proxies=self._proxy)
                if r.status_code != 200:
                    raise Exception("Failed to get initial param.", r.text)

                self._credentials["uuid"] = r.cookies["uuid"]
                self._credentials["token"] = r.cookies["token"]
                self._credentials["random"] = r.cookies["random"]

                if email is not None and password is not None:
                    param = {"mail": email, "password": password}
                    cookie = {"AWSELB": "", "AWSELBCORS": "",
                              **self._credentials}

                    r = s.post("https://www.openrec.tv/viewapp/v4/mobile/user/login",
                               data=param, headers=HEADERS, cookies=cookie, proxies=self._proxy)
                    if r.status_code != 200:
                        raise Exception("Failed to login.", r.text)

                    # self._credentials["sessid"] = r.cookies["PHPSESSID"]
                    self._credentials["access-token"] = r.cookies["access_token"]
                    self._credentials["uuid"] = r.cookies["uuid"]
                    self._credentials["token"] = r.cookies["token"]
                    self._credentials["random"] = r.cookies["random"]
                    self.is_login = True

        self.me()

    def me(self):
        """
        Get login user info.
        """
        if self.is_login:
            url = AUTHORIZED_API + "/users/me"

            info = http.request("GET", url, credentials=self._credentials, proxy=self._proxy)
            if info.status != 200:
                raise Exception(info)

            self.id = info.data[0]["id"]
            self.name = info.data[0]["nickname"]
        else:
            header = {**HEADERS, **self._credentials}
            r = requests.get("https://www.openrec.tv/api-tv/user",
                             headers=header, cookies=self._credentials, proxies=self._proxy)
            j = r.json()
            self.name = j["name"]
