from datetime import datetime

from .utils import http
from .config import EXTERNAL_API, AUTHORIZED_API


def get_comment(vid: str, from_created_at: str, limit=100) -> dict:
    """
    Get comments of live stream.

    param
    -----
    vid: video id
    from_created_at: ISO8601 format datetime (e.g. 2021-12-18T17:48:33+09:00)
    limit: number of comments. max 300
    """
    url = EXTERNAL_API + "/movies/{}/chats".format(vid)
    params = {
        "from_created_at": from_created_at,
        "is_including_system_message": "false",
        "limit": limit
    }
    return http.request("GET", url, params)


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


def get_vod_comment(vid: str) -> dict:
    """
    Get comments of vod

    param
    -----
    vid: video id
    """
    url = EXTERNAL_API + "/movies/{}/comments".format(vid)
    return http.request("GET", url)


def post_comment(vid: str, message: str, credentials) -> dict:
    """
    post a comment to live stream

    param
    -----
    vid: video id
    message: message which you want to post
    credentials: login data
    """
    url = AUTHORIZED_API + "/movies/{}/chats".format(vid)
    params = {
        "message": message,
        "quality_type": 0,
        "league_key": "",
        "to_user_id": "",
        "consented_chat_terms": "false"
    }

    return http.request("POST", url, params, credentials)


def post_vod_comment(vid: str, message: str, credentials) -> dict:
    """
    post a comment to vod

    param
    -----
    vid: video id
    message: message which you want to post
    credentials: login data
    """
    url = AUTHORIZED_API + "/movies/{}/comments".format(vid)
    params = {
        "message": message
    }
    return http.request("POST", url, params, credentials)


def reply_vod_comment(vid: str, comment_id: int, message: str, credentials) -> dict:
    url = AUTHORIZED_API + "/movies/{}/comments/{}/replies".format(vid, str(comment_id))
    params = {
        "message": message,
        "consented_comment_terms": "true"
    }
    return http.request("POST", url, params, credentials)
