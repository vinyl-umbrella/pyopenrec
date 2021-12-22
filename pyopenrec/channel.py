from .util import http
from .util.config import EXTERNAL_API


class Channel:
    """
    - Get current channel ranking.
    - Get user info. (nickname, introduction, register date, and etc.)
    - Get subscription info.
    - Get whether the user is moving or not.
    """

    @staticmethod
    def channel_rank(period, date=None, page=1) -> dict:
        """
        Get current channel ranking.

        param
        -----
        period: "hourly" | "daily" | "weekly" | "monthly"
        date: YYYYMM (e.g. 201912)
        page: page number
        """
        url = EXTERNAL_API + "/channel-ranks"
        params = {
            "period": period,
            "date": date,
            "page": page
        }
        return http.request("GET", url, params)

    @staticmethod
    def channel_info(user_id: str) -> dict:
        """
        Get user info. (nickname, introduction, register date, and etc.)

        param
        -----
        user_id: user id
        """
        url = EXTERNAL_API + "/channels/{}".format(user_id)
        return http.request("GET", url)

    @staticmethod
    def subscription_info(user_id: str) -> dict:
        """
        Get subscription info.

        param
        -----
        user_id: user id
        """
        url = EXTERNAL_API + "/subs-channels/{}".format(user_id)
        return http.request("GET", url)

    @classmethod
    def is_streaming(cls, user_id: str) -> bool:
        """
        Get whether the user is moving or not.

        param
        -----
        user_id: user id
        """
        j = cls.channel_info(user_id)
        if j["status"] == 200 and j["data"]:
            if j["data"]["is_live"]:
                return True
            else:
                return False
        else:
            return False
