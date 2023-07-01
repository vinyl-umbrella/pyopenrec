import requests
from typing import Optional

from .capture import Capture
from .chat import Chat
from .credentials import OpenrecCredentials
from .user import User
from .util import const, exceptions, http, enums
from .video import Video

# from .comment import Comment


class Openrec:
    """
    Openrec class.

    - `Chat()`: get chat object
    - `Capture(capture_id, capture_data)`: get capture object
    - `User(user_id, user_data)`: get user object
    - `Video(video_id, video_data)`: get video object
    - `me()`: get logined user info
    - `have_ng_word(message)`: check if the message has banned word
    - `timeline(type)`: get login user's timeline videos
    """

    credentials: OpenrecCredentials = None

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        if email and password is provided, login to openrec.tv. Otherwise, you can use other functions without login.

        Args:
            email (str): email address
            password (str): password
        """
        if email and password:
            self.credentials = self.__login(email, password)

    def __login(self, email: str, password: str) -> OpenrecCredentials:
        """
        Login to openrec.tv.

        Args:
            email (str): email address
            password (str): password

        Returns:
            OpenrecCredentials: credentials(uuid, token, random, access_token)
        """
        credentials = OpenrecCredentials()
        if not email or not password:
            raise exceptions.PyopenrecException("Email or password is not provided.")

        with requests.session() as s:
            r = s.post(
                "https://www.openrec.tv/api-tv/user",
                headers=const.HEADERS,
            )
            if not r.ok:
                raise exceptions.PyopenrecException(
                    "Failed to get initial param.", r.text
                )

            credentials.uuid = r.cookies.get("uuid", None)
            credentials.token = r.cookies.get("token", None)
            credentials.random = r.cookies.get("random", None)

            param = {"mail": email, "password": password}
            cookie = {
                "AWSELB": "",
                "AWSELBCORS": "",
                "uuid": credentials.uuid,
                "token": credentials.token,
                "random": credentials.random,
            }

            r = s.post(
                "https://www.openrec.tv/viewapp/v4/mobile/user/login",
                data=param,
                headers=const.HEADERS,
                cookies=cookie,
            )
            if not r.ok:
                raise exceptions.PyopenrecException("Failed to login.", r.text)

            # credentials.sessid = r.cookies.get("PHPSESSID")
            credentials.access_token = r.cookies.get("access_token")
            credentials.uuid = r.cookies.get("uuid")
            credentials.token = r.cookies.get("token")
            credentials.random = r.cookies.get("random")

        return credentials

    @staticmethod
    def Chat():
        """
        Get chat object.

        Returns:
            Chat: chat object
        """
        return Chat()

    def Capture(
        self,
        capture_id: str,
        capture_data: Optional[dict] = None,
    ) -> Capture:
        """
        Get capture object.

        Args:
            capture_id (str): capture id
            capture_data (dict): capture data. If you already have capture data, you can skip fetch with this function.

        Returns:
            Capture: capture object
        """
        return Capture(capture_id, capture_data, self.credentials)

    def User(
        self,
        user_id: str,
        user_data: Optional[dict] = None,
    ) -> User:
        """
        Get user object.

        Args:
            user_id (str): user id
            user_data (dict): user data. If you already have user data, you can skip fetch with this function.

        Returns:
            User: user object
        """
        return User(user_id, user_data, self.credentials)

    def Video(
        self,
        video_id: str,
        video_data: Optional[dict] = None,
    ) -> Video:
        """
        Get video object.

        Args:
            video_id (str): video id
            video_data (dict): video data. If you already have video data, you can skip fetch with this function.

        Returns:
            Video: video object
        """
        return Video(video_id, video_data, self.credentials)

    def me(self) -> User:
        """
        Get logined user info.

        Returns:
            User: user object of login user
        """
        if not self.credentials.is_login:
            raise exceptions.AuthException("You need to login.")

        url = f"{const.AUTHORIZED_API}/users/me"
        res = http.get(url, credentials=self.credentials)

        if res.get("status", None) == 0:
            # return res["data"]["items"][0]
            return self.User(
                res["data"]["items"][0]["id"], res["data"]["items"][0], self.credentials
            )
        else:
            raise exceptions.PyopenrecException(f"Error : {res.get('message')}")

    def have_ng_word(self, message: str) -> bool:
        """
        Check if the message has banned word.

        Args:
            message (str): message

        Returns:
            bool: if the message has banned word, return True. otherwise, return False.
        """
        if not self.credentials.is_login:
            raise exceptions.AuthException("You need to login.")

        url = "https://www.openrec.tv/api/v3/user/check_banned_word"
        params = {"nickname": message}
        res = http.get(url, params, self.credentials)

        if res.get("status", None) == 0:
            return bool(res["data"]["has_banned_word"])
        else:
            raise exceptions.PyopenrecException(f"Error : {res.get('message')}")

    def timeline(
        self, type: enums.VideoType = enums.VideoType.coming_up
    ) -> list[Video]:
        """
        Get timeline videos.

        Args:
            type (VideoType): video type. Defaults to `coming_up`.

        Returns:
            list[Video]: list of Video
        """
        if not self.credentials.is_login:
            raise exceptions.AuthException("You need to login.")

        if type == enums.VideoType.coming_up:
            # get coming up videos
            url = f"{const.AUTHORIZED_API}/users/me/timeline-movies/comingups"
            params = {"limit": 40}

            res = http.get(url, params, self.credentials)

            if res.get("status", None) == 0:
                return [self.Video(v["id"], v) for v in res["data"]["items"]]
            else:
                raise exceptions.PyopenrecException(f"Error : {res.get('message')}")

        elif type in [enums.VideoType.live, enums.VideoType.vod]:
            # get live or vod videos
            url = f"{const.AUTHORIZED_API}/users/me/timelines/movies"
            params = {"onair_status": type.value, "limit": 40}
            res = http.get(url, params, self.credentials)

            if res.get("status", None) == 0:
                return [
                    self.Video(v["id"], v) for v in res["data"]["items"][0]["movies"]
                ]
            else:
                raise exceptions.PyopenrecException(f"Error : {res.get('message')}")

        else:
            raise exceptions.PyopenrecException("Invalid type.")
