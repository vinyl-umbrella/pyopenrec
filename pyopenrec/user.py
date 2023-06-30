from typing import Optional

from .openrec import OpenrecCredentials
from .util import const, http
from .util.enums import VideoType


class User:
    credentials: OpenrecCredentials = None

    id: str = ""
    nickname: str = None
    introduciton: str = None
    icon_image_url: str = None
    cover_image_url: str = None
    follows: int = None
    followers: int = None
    is_premium: bool = None
    is_official: bool = None
    is_fresh: bool = None
    is_warned: bool = None
    is_live: bool = None
    live_views: int = None
    registered_at: str = None
    user_status: str = None  # "publish": have streaming authority, "bang": normal user
    views: int = None
    twitter_id: str = None
    # streaming: dict = None

    def __init__(
        self,
        id: str,
        user_data: Optional[dict] = None,
        credentials: Optional[OpenrecCredentials] = None,
    ):
        self.id = id
        self.credentials = credentials
        self.__set_user_info(user_data)

    def __set_user_info(self, user_data: Optional[dict] = None):
        """
        Fetch user info by userid from external api,
        then set user info to self.

        Args:
            user_data (dict): user info from external api
        """
        data = user_data
        if user_data is None:
            url = f"{const.EXTERNAL_API}/channels/{self.id}"
            data = http.get(url)

        self.id = data.get("id", None)
        self.nickname = data.get("nickname", None)
        self.introduciton = data.get("introduction", None)
        self.icon_image_url = data.get("l_icon_image_url", None)
        self.cover_image_url = data.get("l_cover_image_url", None)
        self.follows = data.get("follows", None)
        self.followers = data.get("followers", None)
        self.is_premium = data.get("is_premium", None)
        self.is_official = data.get("is_official", None)
        self.is_fresh = data.get("is_fresh", None)
        self.is_warned = data.get("is_warned", None)
        self.is_live = data.get("is_live", None)
        self.live_views = data.get("live_views", None)
        self.registered_at = data.get("registered_at", None)
        self.user_status = data.get("user_status", None)
        self.views = data.get("views", None)
        self.twitter_id = data.get("twitter_screen_name", None)
        # self.streaming = data.get("onair_broadcast_movies", None)

    def fetch_follows(
        self, sort: Optional[str] = "followed_at", page: int = 1
    ) -> list["User"]:
        """
        Fetch users list of this user follows.
        Args:
            sort (str): "followed_at" or "movie_count" or "movie_published_at"
            page (int): page number
        Returns:
            list: list of users
        """
        url = f"{const.EXTERNAL_API}/users/{self.id}/follows"
        param = {"sort": sort, "page": page}
        folows_list = []
        for user in http.get(url, param):
            folows_list.append(User(user["id"], user))
        return folows_list

    def fetch_followers(self, page: int = 1):
        """
        Fetch users list of this user followers.
        Args:
            page (int): page number
        Returns:
            list: list of users
        """
        url = f"{const.EXTERNAL_API}/users/{self.id}/followers"
        param = {"page": page}
        followers_list = []
        for user in http.get(url, param):
            followers_list.append(User(user["id"], user))
        return followers_list

    def subscription_info(self) -> dict:
        """
        Get subscription info of a specific user.

        Returns:
            dict: subscription info
        """
        url = f"{const.EXTERNAL_API}/subs-channels/{self.id}"
        return http.get(url)

    def contents(
        self, type: VideoType, sort: Optional[str] = "schedule_at", page: int = 1
    ) -> list[dict]:
        """
        Get coming ups, vods and current stream list of a specific user.

        Args:
            user_id: user id
            type: VideoType
            sort: "total_views" or "created_at" or "-created_at" or "schedule_at" or "total_yells" or "-total_yells" or "popularity" or "published_at" or "-published_at"
            page: page number
        Returns:
            list: list of contents
        """
        url = f"{const.EXTERNAL_API}/movies"
        params = {
            "channel_ids": self.id,
            "onair_status": type.value,
            "sort": sort,
            "page": page,
        }
        return http.get(url, params)
