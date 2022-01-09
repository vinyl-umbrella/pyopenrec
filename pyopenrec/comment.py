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
    - Post vote
    """
    is_login = False
    _credentials = None
    _proxy = {}

    def get_comment(self, vid: str, from_created_at=datetime(2020, 1, 1, 0, 0, 0), limit=100) -> dict:
        """
        Get comments of live stream or vod.

        param
        -----
        vid: video id
        from_created_at: datetime
        limit: number of comments. max 300
        """
        url = f"{EXTERNAL_API}/movies/{vid}/chats"
        from_at = from_created_at.astimezone().isoformat(timespec="seconds")
        params = {
            "from_created_at": from_at,
            "is_including_system_message": "false",
            "limit": limit
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def get_recent_comment(self, vid: str, limit=100) -> dict:
        """
        Get recent comments of live stream.

        param
        -----
        vid: video id
        limit: number of comments. max 300
        """
        now = datetime.now().astimezone().isoformat(timespec="seconds")
        url = f"{EXTERNAL_API}/movies/{vid}/chats"

        params = {
            "to_created_at": now,
            "is_including_system_message": "false",
            "limit": limit
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def get_vod_comment(self, vid: str) -> dict:
        """
        Get comments of vod.

        param
        -----
        vid: video id
        """
        url = f"{EXTERNAL_API}/movies/{vid}/comments"
        return http.request("GET", url, proxy=self._proxy)

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
        url = f"{AUTHORIZED_API}/movies/{vid}/chats"
        params = {
            "message": message,
            "quality_type": 0,
            "league_key": "",
            "to_user_id": "",
            "consented_chat_terms": "false"
        }

        return http.request("POST", url, params, self._credentials, proxy=self._proxy)

    def post_template_comment(self, vid: str, comment_num=0) -> dict:
        """
        Post a template comment to live stream.

        param
        -----
        vid: video id
        comment_num:
        0: こんにちは！, 1: こんばんは！, 2: わこつ, 3: 神, 4: ナイス, 5: お疲れ様です！, 6: うまい, 7: おはようございます, 8: 初見です, 9: きたよ, 10: gg, 11: ドンマイ, 12: いいね, 13: おめでとう！, 14: おやすみ
        """
        url = f"https://apiv5.openrec.tv/everyone/api/v5/movies/{vid}/chats"
        comments = [
            "19jlkj1knm7", "lj0gzn767dm", "gje0zy1z7w2", "5n39zmgz41g", "qryvzroz057", "8jw9z3mkrd1", "x9rozpqkm3q", "j9pmkq1zw27", "glew6d8zdmn", "enq56l1zpl4", "o04vz0w6d1m", "1yw4k90knqx", "g9evzxykxd4", "48w2zenzdvj", "q0jl6oekm97"
        ]
        params = {
            "fixed_phrase_id": comments[comment_num],
            "messaged_at": "",
            "quality_type": 2
        }
        return http.request("POST", url, params, self._credentials, proxy=self._proxy)

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

        url = f"{AUTHORIZED_API}/movies/{vid}/comments"
        params = {
            "message": message
        }
        return http.request("POST", url, params, self._credentials, proxy=self._proxy)

    def reply_vod_comment(self, vid: str, comment_id: int, message: str) -> dict:
        """
        Reply to a comment on vod.
        """
        if not self.is_login:
            raise Exception("Login Required.")

        url = f"{AUTHORIZED_API}/movies/{vid}/comments/{str(comment_id)}/replies"
        params = {
            "message": message,
            "consented_comment_terms": "true"
        }
        return http.request("POST", url, params, self._credentials, proxy=self._proxy)

    def post_vote(self, vid: str, vote_id: str, index):
        """
        Post vote

        param
        -----
        vid: video id
        vote_id: vote id. Get from websocket
        index: your choise
        """
        url = f"https://apiv5.openrec.tv/everyone/api/v5/movies/{vid}/polls/{vote_id}/votes"
        params = {"vote_index": index}
        return http.request("POST", url, params, self._credentials, proxy=self._proxy)
