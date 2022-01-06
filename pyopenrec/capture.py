from .util import http
from .util.config import EXTERNAL_API


class Capture:
    """
    - Get popular capture.
    - Get capture list.
    - Get capture info. (title, parent_stream, views, creater, reactions and etc.)
    - Post capture reaction. Login Required.
    """
    _credentials = None
    _proxy = {}

    def popular_capture(self, period="daily", is_channel_unique=True, page=1) -> dict:
        """
        Get popular capture.

        param
        -----
        period: "daily" | "weekly" | "monthly"
        is_channel_unique: Allow duplicate channels or not
        page: page number
        """
        url = f"{EXTERNAL_API}/capture-ranks"
        params = {
            "period": period,
            "is_channel_unique": is_channel_unique,
            "page": page
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def capture_list(self, channel=None, vid=None, sort="views", sort_direction="DESC", page=1) -> dict:
        """
        Get capture list.

        param
        -----
        channel_id: streamer channel id
        vid: video id
        sort: "views" | "public_at" | "reaction"
        sort_direction: "ASC" | "DESC"
        page: page number
        """
        url = f"{EXTERNAL_API}/captures"
        params = {
            "channel_id": channel,
            "movie_id": vid,
            "sort": sort,
            "sort_direction": sort_direction,
            "page": page
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def capture_info(self, cap_id: str) -> dict:
        """
        Get capture info. (title, parent_stream, views, creater, reactions and etc.)

        param
        -----
        cap_id: capture id
        """
        url = f"{EXTERNAL_API}/captures/{cap_id}"
        return http.request("GET", url, proxy=self._proxy)

    def post_capture_reaction(self, cap_id, reaction) -> dict:
        """
        Post capture reaction. Login Required.

        param
        -----
        cap_id: capture id
        reaction: "arara" | "bikkuri" | "gg" | "hatena" | "kakke" | "kami" | "kansya" | "kawaii" | "kusa" | "music" | "nice" | "odoroki" | "sugo" | "tsuyo" | "umai" | "wakuwaku" | "wara" | "yaba"
        """
        if self._credentials is None:
            raise Exception("Login Required.")

        url = "https://apiv5.openrec.tv/everyone/api/v5/reactions"
        params = {
            "target_id": cap_id,
            "target_type": "capture",
            "reaction_id": reaction
        }
        return http.request("POST", url, params, self._credentials, self._proxy)
