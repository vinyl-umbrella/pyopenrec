from .util import http
from .util.config import EXTERNAL_API


class Channel:
    """
    - Get current channel ranking.
    - Get user info. (nickname, introduction, register date, and etc.)
    - Get subscription info.
    - Get `user_id`'s  coming ups, vods and current stream list.
    - get `user_id`'s follow list
    - get `user_id`'s follower list
    - Get whether the user is streaming or not.
    """
    _credentials = None
    _proxy = {}

    def channel_rank(self, period: str, date=None, page=1) -> http.Response:
        """
        Get current channel ranking.

        param
        -----
        period: "hourly" | "daily" | "weekly" | "monthly"
        date: YYYYMM (e.g. 201912)
        page: page number
        """
        url = f"{EXTERNAL_API}/channel-ranks"
        params = {
            "period": period,
            "date": date,
            "page": page
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def channel_info(self, user_id: str) -> http.Response:
        """
        Get user info. (nickname, introduction, register date, and etc.)

        param
        -----
        user_id: user id
        """
        url = f"{EXTERNAL_API}/channels/{user_id}"
        return http.request("GET", url, proxy=self._proxy)

    def subscription_info(self, user_id: str) -> http.Response:
        """
        Get subscription info.

        param
        -----
        user_id: user id
        """
        url = f"{EXTERNAL_API}/subs-channels/{user_id}"
        return http.request("GET", url, proxy=self._proxy)

    def contents(self, user_id: str, type: int, sort="schedule_at", page=1) -> http.Response:
        """
        Get coming ups, vods and current stream list of a specific user.

        param
        -----
        user_id: user id
        type:
            0: coming up
            1: now streaming
            2: vod
        sort:
            "total_views" | "created_at" | "-created_at" | "schedule_at" | "total_yells" | "-total_yells" | "popularity" | "published_at" | "-published_at"
        page: page number
        """
        url = f"{EXTERNAL_API}/movies"
        params = {
            "channel_ids": user_id,
            "onair_status": type,
            "sort": sort,
            "page": page
        }
        return http.request("GET", url, params=params, proxy=self._proxy)

    def get_follow(self, user_id: str, sort="followed_at", page=1) -> http.Response:
        """
        get `user_id`'s follow list

        param
        -----
        user_id: user id
        sort: followed_at || movie_count || movie_published_at
        page: page number
        """
        url = f"{EXTERNAL_API}/users/{user_id}/follows"
        params = {
            "sort": sort,
            "page": page
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def get_follower(self, user_id: str, page=1) -> http.Response:
        """
        get `user_id`'s followers list

        param
        -----
        user_id: user id
        page: page number
        """
        url = f"{EXTERNAL_API}/users/{user_id}/followers"
        params = {
            "page": page
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def is_streaming(self, user_id: str) -> bool:
        """
        Get whether the user is moving or not.

        param
        -----
        user_id: user id
        """
        j = self.channel_info(user_id)
        if j.status == 200 and j.data:
            if j.data["is_live"]:
                return True
            else:
                return False
        else:
            return False
