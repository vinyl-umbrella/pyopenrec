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
    - Get whether the user is moving or not.
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

    def contents(self, user_id: str, type: int) -> http.Response:
        """
        Get coming ups, vods and current stream list of a specific user.

        param
        -----
        user_id: user id
        type:
            0: coming up
            1: now streaming
            2: vod
        """
        url = f"{EXTERNAL_API}/movies"
        params = {
            "channel_ids": user_id,
            "onair_status": type
        }
        return http.request("GET", url, params=params, proxy=self._proxy)

    def _get_follow(self, user_id: str, is_follow: int, page: int) -> http.Response:
        """
        param
        -----
        user_id: user id
        is_follow:
            0: follower
            1: follow
        page: page number
        """
        url = "https://www.openrec.tv/api/v3/get_follow_list"
        recxuser_id = self.channel_info(user_id)["data"]["recxuser_id"]
        params = {
            "recxuser_id": recxuser_id,
            "is_follow": is_follow,
            "page_number": page
        }
        return http.request("GET", url, params, credentials=self._credentials, proxy=self._proxy)

    def get_follow(self, user_id: str, page=1) -> http.Response:
        """
        get `user_id`'s follow list

        param
        -----
        user_id: user id
        page: page number
        """
        return self._get_follow(user_id, 1, page)

    def get_follower(self, user_id: str, page=1) -> http.Response:
        """
        get `user_id`'s followers list

        param
        -----
        user_id: user id
        page: page number
        """
        return self._get_follow(user_id, 0, page)

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
