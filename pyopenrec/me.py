from . import http
from .config import AUTHORIZED_API


def me(credentials) -> dict:
    """
    Get login user info.
    """
    url = AUTHORIZED_API + "/users/me"
    return http.request("GET", url, credentials=credentials)


def timeline(type: int, credentials):
    """
    GET your timeline.

    param
    -----
    type:
        0: coming up
        1: now streaming
        2: vod
    """
    if type == 0:
        url = AUTHORIZED_API + "/users/me/timeline-movies/comingups"
        params = {
            "limit": 40
        }
    elif type == 1 or type == 2:
        url = AUTHORIZED_API + "/users/me/timelines/movies"
        params = {
            "onair_status": type,
            "limit": 40
        }
    else:
        return {"status": 404}

    return http.request("GET", url, params, credentials)
