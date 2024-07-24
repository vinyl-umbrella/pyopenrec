from typing import Optional

from .capture import Capture
from .user import User
from .util import const, http
from .video import Video


class Info:
    @staticmethod
    def capture_rank(
        period: str = "daily", is_channel_unique: bool = True, page: Optional[int] = 1
    ) -> list["Capture"]:
        """
        Get capture rank.

        Args:
            period (str): "daily", "weekly", "monthly"
            is_channel_unique (bool): Allow duplicate channels or not
            page (int): page number

        Returns:
            list[Capture]: list of capture
        """
        url = f"{const.EXTERNAL_API}/capture-ranks"
        params = {
            "period": period,
            "is_channel_unique": is_channel_unique,
            "page": page,
        }
        return [Capture(c["capture"]["id"], c) for c in http.get(url, params)]

    @staticmethod
    def user_rank(period: str, date: Optional[str] = None, page: Optional[int] = 1) -> list["User"]:
        """
        Get current user rank.

        Args:
            period (str): "daily", "weekly", "monthly"
            date (str): yyyyMM (e.g. 202101)
            page (int): page number

        Returns:
            list[User]: list of user
        """
        url = f"{const.EXTERNAL_API}/channel-ranks"
        params = {"period": period, "date": date, "page": page}
        return [User(u["channel"]["id"], u["channel"]) for u in http.get(url, params)]

    @staticmethod
    def stream_rank(page: Optional[int] = 1) -> list["Video"]:
        url = f"{const.EXTERNAL_API}/movies"
        params = {
            "is_live": True,
            "is_upload": False,
            "onair_status": 1,
            "page": page,
            "sort": "live_views",
        }

        return [Video(v["id"], v) for v in http.get(url, params)]

    # @staticmethod
    # def event_list():
    #     pass

    # @staticmethod
    # def event_info():
    #     pass
