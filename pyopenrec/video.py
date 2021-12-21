from .util import http
from .util.config import EXTERNAL_API, AUTHORIZED_API


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


def get_stream_url(vid: str, credentials=None) -> str:
    mdata = video_info(vid)
    if mdata["data"]:
        mdata = mdata["data"]

        # subscription
        if mdata["public_type"] == "member":
            if not credentials:
                return None
            detail = video_detail(vid, credentials)
            if detail["data"]:
                return detail["data"]["data"]["items"][0]["media"]["url"]
        # streaming
        elif mdata["onair_status"] == 1:
            return mdata["media"]["url_ull"]
        # vod
        elif mdata["onair_status"] == 2 and mdata["media"]["url_public"] is not None:
            return mdata["media"]["url_public"].replace(
                "public.m3u8", "playlist.m3u8")
        # uploaded video
        elif mdata["onair_status"] is None and mdata["movie_type"] == "2":
            return mdata["media"]["url"]
        else:
            return None

    return None
