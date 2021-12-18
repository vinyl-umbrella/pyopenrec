from .utils import http
from .config import EXTERNAL_API


def playlists(user_id, type, page=1) -> dict:
    """
    Get playlist list.

    param
    -----
    user_id: user id
    type: "movie" | "capture"
    """
    url = EXTERNAL_API + "/playlists"
    params = {
        "create_user_id": user_id,
        "playlist_type": type,
        "page": page
    }
    return http.request("GET", url, params)


def playlist_contents(playlist_id: str) -> dict:
    """
    Get playlist capture or video list.

    param
    -----
    playlist_id: playlist id
    """
    url = EXTERNAL_API + "/playlists/{}".format(playlist_id)
    return http.request("GET", url)
