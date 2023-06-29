from typing import Optional

from .util import const, enums, http
from .openrec import OpenrecCredentials
from .video import Video
from .user import User


class Capture:
    credentials: OpenrecCredentials = None
    id: str = None
    title: str = None
    is_ban: bool = None
    is_hidden: bool = None
    total_views: int = None
    url: str = None
    thumbnail_url: str = None
    capture_channel: User = None
    video: Video = None
    reactions: list[dict] = None

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
        )
        self.video = Video(data["movie"].get("id"), video_data=data.get("movie"))

    def get_comments():
        pass

    def post_comment():
        pass
