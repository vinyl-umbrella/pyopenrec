import json

from .util import const


# capture.*
# comment.*
# login
# me
# timeline


class OpenrecCredentials:
    access_token: str = None
    uuid: str = None
    token: str = None
    random: str = None

    @property
    def is_login(self) -> bool:
        return (
            self.access_token is not None
            and self.uuid is not None
            and self.token is not None
            and self.random is not None
        )

    @property
    def params(self) -> dict:
        """
        Return credentials as dict.
        """
        return {
            "access_token": self.access_token,
            "uuid": self.uuid,
            "token": self.token,
            "random": self.random,
        }

    def __str__(self) -> str:
        """
        Return credentials as json string.
        """
        return json.dumps(self.params)


def channel_rank(self, period: str, date=None, page=1):
    url = f"{const.EXTERNAL_API}/channel-ranks"
    params = {"period": period, "date": date, "page": page}


def timeline(self, type: int):
    if not self.is_login:
        raise Exception("Login Required.")
    if type == 0:
        url = f"{const.AUTHORIZED_API}/users/me/timeline-movies/comingups"
        params = {"limit": 40}
    elif type in [1, 2]:
        url = f"{const.AUTHORIZED_API}/users/me/timelines/movies"
        params = {"onair_status": type, "limit": 40}
    else:
        raise Exception("Invalid type.")


def has_ng_word(self, word: str) -> bool:
    """
    Check if a word is ng word.

    param
    -----
    word: word you want to check
    """
    if not self.is_login:
        raise Exception("Login Required.")

    url = "https://www.openrec.tv/api/v3/user/check_banned_word"
    params = {"nickname": word}
    # res = http.request("GET", url, params, self._credentials, self._proxy)
    # return bool(res.data["data"]["has_banned_word"])
