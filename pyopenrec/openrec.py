import requests
from typing import Optional

from .etc import OpenrecCredentials
from .chat import Chat
from .user import User
from .video import Video
from .util import const, exceptions

# from .comment import Comment


class Openrec:
    credentials: OpenrecCredentials = None

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Args:
            email (str, optional): email address
            password (str, optional): password
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

    def User(
        self,
        user_id: str,
        user_data: Optional[dict] = None,
    ):
        """
        Get user data.
        Args:
            user_id (str): user id
            user_data (dict, optional): user data. If you already have user data, you can pass it to this function.
        Returns:
            User: user object
        """
        return User(user_id, user_data, self.credentials)

    def Video(
        self,
        video_id: str,
        video_data: Optional[dict] = None,
    ):
        """
        Get video data.
        Args:
            video_id (str): video id
            video_data (dict, optional): video data. If you already have video data, you can pass it to this function.
        Returns:
            Video: video object
        """
        return Video(video_id, video_data, self.credentials)
