from .util import http
from .util.config import EXTERNAL_API, AUTHORIZED_API


class Video:
    """
    - Get current live streamlist.
    - Get popular vod list.
    - Get uploaded video list.
    - Get video info (title, thumbnail, date, owner, game etc.)
    - Get your timeline. Login Required.
    - Get m3u8 url. If your request is member only video, you need to login.
    """
    is_login = False
    _credentials = None
    _proxy = {}

    def stream_list(self, sort="live_views", page=1) -> dict:
        """
        Get current live stream list.

        param
        -----
        page: page number
        sort:
            "total_views" | "created_at" | "-created_at" | "schedule_at" | "onair_status" | "live_views" | "total_yells" | "-total_yells" | "popularity" | "published_at" | "-published_at"
        """
        url = f"{EXTERNAL_API}/movies"
        params = {
            "page": page,
            "onair_status": 1,
            "sort": sort,
            "is_live": "true"
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def vod_list(self, page=1) -> dict:
        """
        Get popular vod list.

        param
        -----
        page: page number
        """
        url = f"{EXTERNAL_API}/popular-movies"
        params = {
            "page": page,
            "popular_type": "archive"
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def movie_list(self, sort="total_views", page=1) -> dict:
        """
        Get uploaded video list.

        param
        -----
        page: page number
        sort:
            "total_views" | "created_at" | "-created_at" | "schedule_at" | "total_yells" | "-total_yells" | "popularity" | "published_at" | "-published_at"
        """
        url = f"{EXTERNAL_API}/movies"
        params = {
            "page": page,
            "sort": sort,
            "is_upload": "true",
            "is_live": "false"
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def video_info(self, vid: str) -> dict:
        """
        Get video info. (title, thumbnail, date, owner, game etc.)

        param
        -----
        vid: video id
        """
        url = f"{EXTERNAL_API}/movies/{vid}"
        return http.request("GET", url, proxy=self._proxy)

    def video_detail(self, vid: str) -> dict:
        """
        Get video detail info.
        If you are using a premium account, you can get stream file url.

        param
        -------
        vid: video id
        """
        if not self.is_login:
            raise Exception("Login Required.")

        url = f"{AUTHORIZED_API}/movies/{vid}/detail"
        return http.request("GET", url, credentials=self._credentials, proxy=self._proxy)

    def timeline(self, type: int):
        """
        Get your timeline. Login Required.

        param
        -----
        type:
            0: coming up
            1: now streaming
            2: vod
        """
        if not self.is_login:
            raise Exception("Login Required.")
        if type == 0:
            url = f"{AUTHORIZED_API}/users/me/timeline-movies/comingups"
            params = {
                "limit": 40
            }
        elif type in [1, 2]:
            url = f"{AUTHORIZED_API}/users/me/timelines/movies"
            params = {
                "onair_status": type,
                "limit": 40
            }
        else:
            return {"status": 404}

        return http.request("GET", url, params, self._credentials, proxy=self._proxy)

    def get_stream_url(self, vid: str) -> str:
        """
        Get m3u8 url. If your request is member only video, you need to login.

        param
        -----
        vid: video id
        """
        mdata = self.video_info(vid)
        if mdata["data"]:
            mdata = mdata["data"]

            # subscription
            if mdata["public_type"] == "member":
                if not self.is_login:
                    raise Exception("Login Required.")

                detail = self.video_detail(vid)
                if detail["data"]:
                    return detail["data"]["data"]["items"][0]["media"]["url"]
            # streaming
            elif mdata["onair_status"] == 1:
                return mdata["media"]["url_ull"]
            # vod
            elif mdata["onair_status"] == 2 and mdata["media"]["url_public"] is not None:
                return mdata["media"]["url_public"].replace(
                    "public.m3u8", "playlist.m3u8")
            # uploaded video
            elif mdata["onair_status"] is None and mdata["movie_type"] == "2":
                return mdata["media"]["url"]
            else:
                return ""

        return ""
