from typing import Optional

from .comment import Comment
from .credentials import OpenrecCredentials
from .user import User
from .util import const, enums, exceptions, http
from .video import Video


class Capture:
    """
    Capture class.

    - `get_comments()`: get comments for capture
    - `post_comment(message)`: post comment to capture
    - `post_reaction(reaction_type)`: post reaction to capture
    """

    credentials: Optional[OpenrecCredentials] = None
    id: Optional[str] = None
    title: Optional[str] = None
    is_ban: Optional[bool] = None
    is_hidden: Optional[bool] = None
    total_views: Optional[int] = None
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    capture_channel: Optional[User] = None
    video: Optional[Video] = None
    reactions: Optional[dict[enums.ReactionType, int]] = {}

    def __init__(
        self,
        id: str,
        capture_data: Optional[dict] = None,
        credentials: Optional[OpenrecCredentials] = None,
    ):
        self.id = id
        self.credentials = credentials
        self.__set_capture_info(capture_data)

    def __set_capture_info(self, capture_data: Optional[dict] = None):
        data = capture_data
        if capture_data is None:
            url = f"{const.EXTERNAL_API}/captures/{self.id}"
            data = http.get(url)

        if not isinstance(data, dict):
            raise AssertionError("Unexpected response.")

        self.id = data["capture"].get("id", None)
        self.title = data["capture"].get("title", None)
        self.is_ban = data["capture"].get("is_ban", None)
        self.is_hidden = data["capture"].get("is_hidden", None)
        self.total_views = data["capture"].get("total_views", None)
        self.url = (
            "https://public.openrec.tv" + data["capture"].get("url", None)
            if data["capture"].get("url", None)
            else None
        )
        self.thumbnail_url = data.get("thumbnail_url", None)
        self.capture_channel = User(
            data["capture_channel"].get("id"),
            user_data=data.get("capture_channel"),
            credentials=self.credentials,
        )
        self.video = Video(
            data["movie"].get("id"),
            video_data=data.get("movie"),
            credentials=self.credentials,
        )

        for r in data["reaction_stats_list"]:
            self.reactions[enums.ReactionType(r["id"]).name] = r["count"]

    def get_comments(self) -> list[Comment]:
        """
        Get comments for capture.

        Returns:
            list[Comment]: list of Comment
        """
        url = f"{const.EXTERNAL_API}/captures/{self.id}/comments"
        return [Comment(comment_from_rest=comment) for comment in http.get(url)]

    def post_comment(self, message: str) -> dict:
        """
        Post comment to capture.

        Args:
            message (str): message you want to post

        Returns:
            dict: posted comment info
        """
        if not self.credentials:
            raise exceptions.AuthException("You need to login.")

        url = f"{const.AUTHORIZED_API}/captures/{self.id}/comments"
        params = {"message": message, "consented_comment_terms": True}
        d = http.post(url, params, self.credentials)
        if not isinstance(d, dict):
            raise AssertionError("Unexpected response.")
        return d

    def post_reaction(self, reaction_type: enums.ReactionType) -> dict:
        """
        Post reaction to capture.

        Args:
            reaction_type (ReactionType): reaction type
        Returns:
            dict: reaction info
        """
        url = "https://apiv5.openrec.tv/everyone/api/v5/reactions"
        data = {
            "target_id": self.id,
            "target_type": "capture",
            "reaction_id": reaction_type.name,
        }
        d = http.post(url, data, self.credentials)
        if not isinstance(d, dict):
            raise AssertionError("Unexpected response.")
        return d
