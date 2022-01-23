from .util import http
from .util.config import EXTERNAL_API


class Playlist:
    """
    - Get list of playlists for a specific user.
    - Get playlist contents, capture or video.
    """
    _proxy = {}

    def playlists(self, user_id, type, page=1) -> http.Response:
        """
        Get list of playlists for a specific user.

        param
        -----
        user_id: user id
        type: "movie" | "capture"
        """
        url = f"{EXTERNAL_API}/playlists"
        params = {
            "create_user_id": user_id,
            "playlist_type": type,
            "page": page
        }
        return http.request("GET", url, params, proxy=self._proxy)

    def playlist_contents(self, playlist_id: str) -> http.Response:
        """
        Get playlist contents, capture or video.

        param
        -----
        playlist_id: playlist id
        """
        url = f"{EXTERNAL_API}/playlists/{playlist_id}"
        return http.request("GET", url, proxy=self._proxy)
