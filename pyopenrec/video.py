from datetime import datetime
from typing import Optional

from .comment import Comment
from .credentials import OpenrecCredentials
from .user import User
from .util import const, exceptions, http
from .util.enums import VideoType


class Video:
    credentials: OpenrecCredentials = None
    id: str = None
    movie_id: int = None
    title: str = None
    introduction: str = None
    is_hidden: bool = None
    is_live: bool = None
    on_air_status: VideoType = None
    thumnail_url: str = None
    live_views: int = None
    total_views: int = None
    total_yells: int = None
    created_at: str = None
    published_at: str = None
    started_at: str = None
    tags: list[str] = None
    media_url: str = None
    user: "User" = None

    def __init__(
        self,
        id: str,
        video_data: Optional[dict] = None,
        credentials: Optional[OpenrecCredentials] = None,
    ):
        """
        Args:
            id (str): video id
            video_data (dict, optional): video info as dict
            credentials (OpenrecCredentials, optional): login credentials
        """
        self.id = id
        self.credentials = credentials
        self.__set_video_info(video_data)

    def __set_video_info(self, video_data: Optional[dict] = None):
        """
        Fetch video info by video id from external api,
        then set video info to self.

        Args:
            video_data (dict): video info as dict
        """
        data = video_data
        if video_data is None:
            url = f"{const.EXTERNAL_API}/movies/{self.id}"
            data = http.get(url)

        self.id = data.get("id", None)
        self.movie_id = data.get("movie_id", None)
        self.title = data.get("title", None)
        self.introduction = data.get("introduction", None)
        self.is_hidden = data.get("is_hidden", None)
        self.is_live = data.get("is_live", None)
        self.on_air_status = VideoType(data.get("onair_status", None))
        self.thumnail_url = data.get("l_thumbnail_url", None)
        self.live_views = data.get("live_views", None)
        self.total_views = data.get("total_views", None)
        self.total_yells = data.get("total_yells", None)
        self.created_at = data.get("created_at", None)
        self.published_at = data.get("published_at", None)
        self.started_at = data.get("started_at", None)
        self.tags = data.get("tags", None)
        self.user = User(
            data["channel"]["id"], data.get("channel", None), self.credentials
        )

        # live
        if self.on_air_status == VideoType.live:
            self.media_url = data["media"]["url_ull"]
        # vod
        elif (
            self.on_air_status == VideoType.vod
            and data["media"]["url_public"] is not None
        ):
            self.media_url = data["media"]["url_public"].replace(
                "public.m3u8", "playlist.m3u8"
            )
        # uploaded video
        elif self.on_air_status is None and data["movie_type"] == "2":
            self.media_url = data["media"]["url"]

    def yell_rank(self, page: int = 1) -> list[dict]:
        """
        get yell rank of live stream.

        Args:
            page (int, optional): page number.

        Returns:
            list[dict]: yell rank info
        """
        url = f"{const.EXTERNAL_API}/yell-ranks"
        params = {"movie_id": self.id, "page": page}
        # TODO: yell classを作ってまとめたい
        return http.get(url, params)

    def yell_history(self, page: int = 1) -> list[dict]:
        """
        get yell history of live stream.

        Args:
            page (int, optional): page number.

        Returns:
            list[dict]: yell history info
        """
        url = f"{const.EXTERNAL_API}/yell-logs"
        params = {"movie_id": self.id, "page": page}
        # TODO: yell classを作ってまとめたい
        return http.get(url, params)

    def get_comments(
        self,
        from_created_at: datetime = datetime(2000, 1, 1, 0, 0, 0),
        limit: int = 100,
    ) -> list["Comment"]:
        """
        Get comments of live stream or vod.

        Args:
            from_created_at (datetime, optional): datetime object.
            limit (int, optional): number of comments. max 300

        Returns:
            list[Comment]: list of Comment object
        """
        url = f"{const.EXTERNAL_API}/movies/{self.id}/chats"
        from_at = from_created_at.astimezone().isoformat(timespec="seconds")
        params = {
            "from_created_at": from_at,
            "is_including_system_message": "false",
            "limit": limit,
        }

        return [Comment(comment_from_rest=comment) for comment in http.get(url, params)]

    def get_recent_comments(self, limit: int = 100) -> list["Comment"]:
        """
        Get recent comments of live stream.

        Args:
            limit (int): number of comments. max 300

        Returns:
            list[Comment]: list of Comment object
        """
        now = datetime.now().astimezone().isoformat(timespec="seconds")
        url = f"{const.EXTERNAL_API}/movies/{self.id}/chats"

        params = {
            "to_created_at": now,
            "is_including_system_message": "false",
            "limit": limit,
        }

        return [Comment(comment_from_rest=comment) for comment in http.get(url, params)]

    def get_vod_comments(self) -> list["Comment"]:
        """
        Get comments of vod.

        Returns:
            list[Comment]: list of Comment object
        """
        url = f"{const.EXTERNAL_API}/movies/{self.id}/comments"

        return [Comment(comment_from_rest=comment) for comment in http.get(url)]

    def post_comment(self, message: str) -> dict:
        """
        Post a comment to live stream.

        Args:
            message (str): message which you want to post

        Returns:
            dict: post result
        """
        if not self.credentials.is_login:
            raise exceptions.AuthException("You need to login.")

        url = f"{const.AUTHORIZED_API}/movies/{self.id}/chats"
        params = {
            "message": message,
            "quality_type": 0,
            "league_key": "",
            "to_user_id": "",
            "consented_chat_terms": "false",
        }
        return http.post(url, params, self.credentials)

    # def post_template_comment(self, comment_id: int) -> dict:
    #     """
    #     Post a template comment to live stream.

    #     Args:
    #         comment_id (int, optional): comment id.
    #         0: こんにちは！, 1: こんばんは！, 2: わこつ, 3: 神, 4: ナイス, 5: お疲れ様です！, 6: うまい, 7: おはようございます, 8: 初見です, 9: きたよ, 10: gg, 11: ドンマイ, 12: いいね, 13: おめでとう！, 14: おやすみ
    #     """
    #     url = f"https://apiv5.openrec.tv/everyone/api/v5/movies/{self.id}/chats"
    #     template_comments = [
    #         "19jlkj1knm7",
    #         "lj0gzn767dm",
    #         "gje0zy1z7w2",
    #         "5n39zmgz41g",
    #         "qryvzroz057",
    #         "8jw9z3mkrd1",
    #         "x9rozpqkm3q",
    #         "j9pmkq1zw27",
    #         "glew6d8zdmn",
    #         "enq56l1zpl4",
    #         "o04vz0w6d1m",
    #         "1yw4k90knqx",
    #         "g9evzxykxd4",
    #         "48w2zenzdvj",
    #         "q0jl6oekm97",
    #     ]
    #     params = {
    #         "fixed_phrase_id": template_comments[comment_id],
    #         "messaged_at": "",
    #         "quality_type": 2,
    #     }
    #     return http.post(url, params, self.credentials)

    def post_vod_comment(self, message: str) -> dict:
        """
        Post a comment to vod.

        Args:
            message (str): message which you want to post

        Returns:
            dict: post result
        """
        if not self.credentials.is_login:
            raise exceptions.AuthException("You need to login.")
        url = f"{const.AUTHORIZED_API}/movies/{self.id}/comments"
        params = {"message": message}
        return http.post(url, params, self.credentials)

    def post_vote(self, vote_id: str, index: int) -> dict:
        """
        Post a vote to live stream.

        Args:
            vote_id (str): vote id
            index (int): index of vote

        Returns:
           dict: vote result
        """

        url = f"https://apiv5.openrec.tv/everyone/api/v5/movies/{self.id}/votes/{vote_id}/votes"
        params = {"vote_index": index}
        return http.post(url, params, self.credentials)
