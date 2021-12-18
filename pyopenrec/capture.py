from .utils import http
from .config import EXTERNAL_API


def popular_capture(period="daily", is_channel_unique=True, page=1) -> dict:
    """
    Get popular capture.

    param
    -----
    period: "daily" | "weekly" | "monthly"
    is_channel_unique: Allow duplicate channels or not
    page: page number
    """
    url = EXTERNAL_API + "/capture-ranks"
    params = {
        "period": period,
        "is_channel_unique": is_channel_unique,
        "page": page
    }
    return http.request("GET", url, params)


def capture_list(channel=None, vid=None, sort="views", sort_direction="DESC", page=1) -> dict:
    """
    Get capture list.

    param
    -----
    channel_id: streamer channel id
    vid: video id
    sort: "views" | "public_at" | "reaction"
    sort_direction: "ASC" | "DESC"
    page: page number
    """
    url = EXTERNAL_API + "/captures"
    params = {
        "channel_id": channel,
        "movie_id": vid,
        "sort": sort,
        "sort_direction": sort_direction,
        "page": page
    }
    return http.request("GET", url, params)


def capture_info(cap_id: str) -> dict:
    """
    Get capture info. (title, parent_stream, views, creater, reactions and etc.)

    param
    -----
    cap_id: capture id
    """
    url = EXTERNAL_API + "/captures/{}".format(cap_id)
    return http.request("GET", url)


def post_capture_reaction(cap_id, reaction, credentials) -> dict:
    """
    Post capture reaction.

    param
    -----
    cap_id: capture id
    reaction: "arara" | "bikkuri" | "gg" | "hatena" | "kakke" | "kami" | "kansya" | "kawaii" | "kusa" | "music" | "nice" | "odoroki" | "sugo" | "tsuyo" | "umai" | "wakuwaku" | "wara" | "yaba"
    """
    url = "https://apiv5.openrec.tv/everyone/api/v5/reactions"
    params = {
        "target_id": cap_id,
        "target_type": "capture",
        "reaction_id": reaction
    }
    return http.request("POST", url, params, credentials)
