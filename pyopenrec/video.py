from .utils import http
from .config import EXTERNAL_API


def get_stream_list(sort="live_views", page=1) -> dict:
    """
    get current live stream list

    param
    ----------
    page: int
        page number
    sort: str
        "total_views" | "created_at" | "-created_at" | "schedule_at" | "onair_status" | "live_views" | "total_yells" | "-total_yells" | "popularity" | "published_at" | "-published_at"
    """
    url = EXTERNAL_API + "/movies"
    params = {
        "page": page,
        "onair_status": 1,
        "sort": sort,
        "is_live": "true"
    }
    res = http.get(url, params=params)
    return res


def get_vod_list(page=1) -> dict:
    """
    get popular vod list

    param
    ----------
    page: int
        page number
    sort: str
        "total_views" | "created_at" | "-created_at" | "schedule_at" | "onair_status" | "live_views" | "total_yells" | "-total_yells" | "popularity" | "published_at" | "-published_at"
    """
    url = EXTERNAL_API + "/popular-movies"
    params = {
        "page": page,
        "popular_type": "archive"
    }
    res = http.get(url, params=params)
    return res


def get_movie_list(sort="total_views", page=1) -> dict:
    """
    get video list

    param
    ----------
    page: int
        page number
    sort: str
        "total_views" | "created_at" | "-created_at" | "schedule_at" | "total_yells" | "-total_yells" | "popularity" | "published_at" | "-published_at"
    """
    url = EXTERNAL_API + "/movies"
    params = {
        "page": page,
        "sort": sort,
        "is_upload": "true",
        "is_live": "false"
    }
    res = http.get(url, params=params)
    return res


def get_video_info(vid: str) -> dict:
    """
    get video info (title, thumbnail, date, owner, game etc.)

    param
    ----------
    vid: str
        video id
    """
    url = EXTERNAL_API + "/movies/" + vid
    return http.get(url)
