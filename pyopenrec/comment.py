from datetime import datetime

from .util import http
from .util.config import EXTERNAL_API, AUTHORIZED_API


class Comment:
    """
    - Get comments of live stream or vod.
    - Get recent comments of live stream.
    - Get comments of vod.
    - Post a comment to live stream.
    - Post a comment to vod.
    - Reply to a comment on vod.
    """
    is_login = False
    _credentials = None

    @staticmethod
    def get_comment(vid: str, from_created_at=datetime(2020, 1, 1, 0, 0, 0), limit=100) -> dict:
        """
        Get comments of live stream or vod.

        param
        -----
        vid: video id
        from_created_at: datetime
        limit: number of comments. max 300
        """
        url = EXTERNAL_API + "/movies/{}/chats".format(vid)
        from_at = from_created_at.astimezone().isoformat(timespec="seconds")
        params = {
            "from_created_at": from_at,
            "is_including_system_message": "false",
            "limit": limit
        }
        return http.request("GET", url, params)

    @staticmethod
    def get_recent_comment(vid: str, limit=100) -> dict:
        """
        Get recent comments of live stream.

        param
        -----
        vid: video id
        limit: number of comments. max 300
        """
        now = datetime.now().astimezone().isoformat(timespec="seconds")
        url = EXTERNAL_API + "/movies/{}/chats".format(vid)

        params = {
            "to_created_at": now,
            "is_including_system_message": "false",
            "limit": limit
        }
        return http.request("GET", url, params)

    @staticmethod
    def get_vod_comment(vid: str) -> dict:
        """
        Get comments of vod.

        param
        -----
        vid: video id
        """
        url = EXTERNAL_API + "/movies/{}/comments".format(vid)
        return http.request("GET", url)

    def post_comment(self, vid: str, message: str) -> dict:
        """
        Post a comment to live stream.

        param
        -----
        vid: video id
        message: message which you want to post
        """
        if not self.is_login:
            raise Exception("Login Required.")
        url = AUTHORIZED_API + "/movies/{}/chats".format(vid)
        params = {
            "message": message,
            "quality_type": 0,
            "league_key": "",
            "to_user_id": "",
            "consented_chat_terms": "false"
        }

        return http.request("POST", url, params, self._credentials)

    def post_template_comment(self, vid: str, comment_num=0) -> dict:
        """
        Post a template comment to live stream.

        param
        -----
        vid: video id
        comment_num:
        0: こんにちは！, 1: こんばんは！, 2: わこつ, 3: 神, 4: ナイス, 5: お疲れ様です！, 6: うまい, 7: おはようございます, 8: 初見です, 9: きたよ, 10: gg, 11: ドンマイ, 12: いいね, 13: おめでとう！, 14: おやすみ
        """
        url = "https://apiv5.openrec.tv/everyone/api/v5/movies/{}/chats".format(vid)
        comments = [
            "19jlkj1knm7", "lj0gzn767dm", "gje0zy1z7w2", "5n39zmgz41g", "qryvzroz057", "8jw9z3mkrd1", "x9rozpqkm3q", "j9pmkq1zw27", "glew6d8zdmn", "enq56l1zpl4", "o04vz0w6d1m", "1yw4k90knqx", "g9evzxykxd4", "48w2zenzdvj", "q0jl6oekm97"
        ]
        params = {
            "fixed_phrase_id": comments[comment_num],
            "messaged_at": "",
            "quality_type": 2
        }
        return http.request("POST", url, params, self._credentials)

    def post_vod_comment(self, vid: str, message: str) -> dict:
        """
        Post a comment to vod.

        param
        -----
        vid: video id
        message: message which you want to post
        """
        if not self.is_login:
            raise Exception("Login Required.")

        url = AUTHORIZED_API + "/movies/{}/comments".format(vid)
        params = {
            "message": message
        }
        return http.request("POST", url, params, self._credentials)

    def reply_vod_comment(self, vid: str, comment_id: int, message: str) -> dict:
        """
        Reply to a comment on vod.
        """
        if not self.is_login:
            raise Exception("Login Required.")

        url = AUTHORIZED_API + \
            "/movies/{}/comments/{}/replies".format(vid, str(comment_id))
        params = {
            "message": message,
            "consented_comment_terms": "true"
        }
        return http.request("POST", url, params, self._credentials)
