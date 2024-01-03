from typing import Optional

from .credentials import OpenrecCredentials
from .util import const, http
from .util.enums import VideoType


class User:
    """
    User class.

    - `follows()`: get users list of this user follows
    - `followers(sort, page)`: get users list of this user followers
    - `subscription_info(page)`: get subscription info of a specific user
    - `contents(type, sort, page)`: get coming ups, vods and current stream list of a specific user
    - `captures(sort_direction, page)`: get captures list of a specific user
    - `capture_rank(period, page)`: get capture rank of a specific user
    - `yell_rank(month, page)`: get yell rank of a specific user
    - `board_items()`: get board items of a specific user
    """

    credentials: OpenrecCredentials = None

    id: str = ""
    recxuser_id: str = None
    nickname: str = None
    introduciton: str = None
    icon_image_url: str = None
    cover_image_url: str = None
    follows_num: int = None
    followers_num: int = None
    is_premium: bool = None
    is_official: bool = None
    is_fresh: bool = None
    is_warned: bool = None
    is_live: bool = None
    live_views: int = None
    registered_at: str = None
    user_status: str = None  # "publish": have streaming authority, "bang": normal user
    user_color: str = None
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
        self.recxuser_id = data.get("recxuser_id", None)
        self.nickname = data.get("nickname", None)
        self.introduciton = data.get("introduction", None)
        self.icon_image_url = data.get("l_icon_image_url", None)
        self.cover_image_url = data.get("l_cover_image_url", None)
        self.follows_num = data.get("follows", None)
        self.followers_num = data.get("followers", None)
        self.is_premium = data.get("is_premium", None)
        self.is_official = data.get("is_official", None)
        self.is_fresh = data.get("is_fresh", None)
        self.is_warned = data.get("is_warned", None)
        self.is_live = data.get("is_live", None)
        self.live_views = data.get("live_views", None)
        self.registered_at = data.get("registered_at", None)
        self.user_status = data.get("user_status", None)
        self.user_color = data.get("user_color", None)
        self.views = data.get("views", None)
        self.twitter_id = data.get("twitter_screen_name", None)
        # self.streaming = data.get("onair_broadcast_movies", None)

    def follows(
        self, sort: Optional[str] = "followed_at", page: int = 1
    ) -> list["User"]:
        """
        Fetch users list of this user follows.

        Args:
            sort (str): "followed_at" or "movie_count" or "movie_published_at"
            page (int): page number

        Returns:
            list[User]: list of users
        """
        url = f"{const.EXTERNAL_API}/users/{self.id}/follows"
        param = {"sort": sort, "page": page}

        return [
            User(user["id"], user, self.credentials) for user in http.get(url, param)
        ]

    def followers(self, page: int = 1) -> list["User"]:
        """
        Fetch users list of this user followers.

        Args:
            page (int): page number

        Returns:
            list[User]: list of users
        """
        url = f"{const.EXTERNAL_API}/users/{self.id}/followers"
        param = {"page": page}

        return [
            User(user["id"], user, self.credentials) for user in http.get(url, param)
        ]

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
            type (VideoType): VideoType
            sort (str): "total_views" or "created_at" or "-created_at" or "schedule_at" or "total_yells" or "-total_yells" or "popularity" or "published_at" or "-published_at"
            page (int): page number

        Returns:
            list[dict]: list of contents # TODO: return Video object
        """
        url = f"{const.EXTERNAL_API}/movies"
        params = {
            "channel_ids": self.id,
            "onair_status": type.value,
            "sort": sort,
            "page": page,
        }
        return http.get(url, params)

    def captures(
        self,
        sort_direction: Optional[str] = "DESC",
        page: int = 1,
    ) -> list[dict]:
        """
        Get captures list of a specific user.

        Args:
            sort_direction (str): "ASC" or "DESC"
            page (int): page number

        Returns:
            list[dict]: list of captures # TODO: Captureを返したい
        """
        url = f"{const.EXTERNAL_API}/captures"
        params = {
            "channel_ids": self.id,
            "sort": "public_at",
            "sort_direction": sort_direction,
            "page": page,
        }

        return http.get(url, params)

    def capture_rank(
        self, preriod: Optional[str] = "weekly", page: Optional[int] = 1
    ) -> list[dict]:
        """
        Get capture rank of a specific user.

        Args:
            user_id (str): user id
            preriod (str): "daily" or "weekly" or "monthly"
            page (int): page number

        Returns:
            list[dict]: list of captures # TODO: Captureを返したい
        """

        url = f"{const.EXTERNAL_API}/capture-ranks"
        params = {
            "channel_ids": self.id,
            "period": preriod,
            "page": page,
        }
        return http.get(url, params)

    def yell_rank(self, month: Optional[str], page: int = 1) -> list[dict]:
        """
        Get yell rank of a specific user.

        Args:
            month (str): yyyyMM. if month is empty, return all yell rank.

        Returns:
            list[dict]: list of yell rank
        """
        url = f"{const.EXTERNAL_API}/yell-ranks"
        params = {
            "user_id": self.id,
            "month": month,
            "page": page,
        }

        l = []
        for rank in http.get(url, params):
            rank["user"] = User(rank["user"]["id"], rank["user"], self.credentials)
            rank["to_user"] = User(
                rank["to_user"]["id"], rank["to_user"], self.credentials
            )
            l.append(rank)
        return l

    def board_items(self) -> list[dict]:
        """
        Get board items of a specific user.

        Returns:
            list[dict]: list of board items
        """
        url = f"{const.EXTERNAL_API}/ext-board/users/{self.id}/board-items"
        params = {"board_type": "custom-board", "page": 1}

        return http.get(url, params)
