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
        self.session = requests.session()
        r = self.session.post("https://www.openrec.tv/api-tv/user",
                              headers=HEADERS)
        if r.status_code != 200:
            raise Exception("failed to get param")

        self._credentials["uuid"] = r.cookies["uuid"]
        self._credentials["token"] = r.cookies["token"]
        self._credentials["random"] = r.cookies["random"]

        if email is not None and password is not None:
            param = {
                "mail": email,
                "password": password
            }

            r = self.session.post("https://www.openrec.tv/viewapp/v4/mobile/user/login",
                                  data=param, headers=HEADERS, cookies=self._credentials)
            if r.status_code != 200:
                raise Exception("failed to login")

            # self._credentials["sessid"] = r.cookies["PHPSESSID"]
            self._credentials["access-token"] = r.cookies["access_token"]
            self.is_login = True

        self.me()

    def me(self) -> dict:
        """
        Get login user info.
        """
        url = AUTHORIZED_API + "/users/me"

        info = http.request("GET", url, credentials=self._credentials)
        if info["status"] != 200:
            raise Exception(info)

        # print(info)
        self.id = info["data"]["items"]["id"]
        self.name = info["data"]["items"]["nickname"]
