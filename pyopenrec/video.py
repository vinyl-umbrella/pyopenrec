from . import http
from .config import EXTERNAL_API, AUTHORIZED_API


def stream_list(sort="live_views", page=1) -> dict:
    """
    Get current live stream list.

    param
    ----------
    page: page number
    sort:
        "total_views" | "created_at" | "-created_at" | "schedule_at" | "onair_status" | "live_views" | "total_yells" | "-total_yells" | "popularity" | "published_at" | "-published_at"
    """
    url = EXTERNAL_API + "/movies"
    params = {
        "page": page,
        "onair_status": 1,
        "sort": sort,
        "is_live": "true"
    }
    return http.request("GET", url, params)


def vod_list(page=1) -> dict:
    """
    Get popular vod list.

    param
    ----------
    page: page number
    """
    url = EXTERNAL_API + "/popular-movies"
    params = {
        "page": page,
        "popular_type": "archive"
    }
    return http.request("GET", url, params)


def movie_list(sort="total_views", page=1) -> dict:
    """
    Get uploaded video list.

    param
    ----------
    page: page number
    sort:
        "total_views" | "created_at" | "-created_at" | "schedule_at" | "total_yells" | "-total_yells" | "popularity" | "published_at" | "-published_at"
    """
    url = EXTERNAL_API + "/movies"
    params = {
        "page": page,
        "sort": sort,
        "is_upload": "true",
        "is_live": "false"
    }
    return http.request("GET", url, params)


def video_info(vid: str) -> dict:
    """
    Get video info (title, thumbnail, date, owner, game etc.).

    param
    ----------
    vid: video id
    """
    url = EXTERNAL_API + "/movies/" + vid
    return http.request("GET", url)


def video_detail(vid: str, credentials) -> dict:
    """
    Get video detail info.
    If you are using a premium account, you can get stream file url.

    param
    -------
    vid: video id
    credentials: login data

    """
    url = AUTHORIZED_API + "/movies/{}/detail".format(vid)
    return http.request("GET", url, credentials=credentials)
