from .util import http
from .util.config import EXTERNAL_API


class Yell:
    """
    - Get yell list in the order of points in a specific video.
    - Get yell list in the order of points in a specific user.
    - Get yell list in time order.
    """
    @staticmethod
    def yell_rank_in_video(vid: str, page=1):
        """
        Get yell list in the order of points in a specific video.

        param
        -----
        vid: video id
        page: page number
        """
        url = EXTERNAL_API + "/yell-ranks"
        params = {
            "movie_id": vid,
            "page": page
        }
        return http.request("GET", url, params)

    @staticmethod
    def yell_rank_in_user(user_id: str, month=None, page=1):
        """
        Get yell list in the order of points in a specific user.

        param
        -----
        user_id: user id
        month: \\d{6}
        page: page number
        """
        url = EXTERNAL_API + "/yell-ranks"
        params = {
            "user_id": user_id,
            "month": str(month),
            "page": page
        }
        return http.request("GET", url, params)

    @staticmethod
    def yell_history(vid, page=1):
        """
        Get yell list in time order.

        param
        -----
        vid: video id
        page: page number
        """
        url = EXTERNAL_API + "/yell-logs"
        params = {
            "movie_id": vid,
            "page": page
        }
        return http.request("GET", url, params)
