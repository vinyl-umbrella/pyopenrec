import requests
from .config import Config


class Openrec(Config):
    def popular_capture(self, period="daily", page=1, is_channel_unique="false", proxy=None) -> dict:
        """
        period
            daily
            weekly
            monthly
        """
        url = self.PUB_API + self.CAPTURERANK_PATH
        param = {
            "period": period,
            "page": page,
            "is_channel_unique": is_channel_unique,
        }

        retval = 0
        j = {}
        try:
            j = requests.get(url, headers=self.HEADERS, params=param, proxies=proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}

    def get_user_info(self, user_id: str, proxy=None) -> dict:
        url = self.PUB_API + self.CHANNEL_PATH + user_id
        retval = 0
        j = {}
        try:
            j = requests.get(url, headers=self.HEADERS, proxies=proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}

    def get_onair_movie(self, page=1, sort="live_views", onair_status=1, proxy=None) -> dict:
        """
        sort
            live_views: 同接順
            -total_yells: エール順
        onair_status
            0: 予約枠
            1: 配信中
        """
        url = self.PUB_API + self.MOVIES_PATH
        param = {
            "is_live": True,
            "onair_status": onair_status,
            "page": page,
            "sort": sort
        }

        retval = 0
        j = {}
        try:
            j = requests.get(url, headers=self.HEADERS, params=param, proxies=proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}


class User(Openrec):
    is_login = False

    def __init__(self, email=None, password=None, proxy=None):
        self.proxy = proxy
        if email is not None and password is not None:
            with requests.Session() as s:
                r = s.post("https://www.openrec.tv/api-tv/user", headers=self.HEADERS, proxies=self.proxy)
                # login
                param = {
                    "mail": email,
                    "password": password
                }
                cookie = {
                    "Uuid": r.cookies["uuid"],
                    "Token": r.cookies["token"],
                    "Random": r.cookies["random"],
                    "_gcl_au": "",
                    "AWSELB": "",
                    "AWSELBCORS": ""
                }

                r = s.post("https://www.openrec.tv/viewapp/v4/mobile/user/login", data=param, headers=self.HEADERS, cookies=cookie, proxies=proxy)

                self.__uuid = r.cookies["uuid"]
                self.__token = r.cookies["token"]
                self.__random = r.cookies["random"]
                self.__phpsessid = r.cookies["PHPSESSID"]
                self.__access_token = r.cookies["access_token"]
                self.is_login = True

    def post_comment(self, video_id: str, message: str) -> dict:
        url = "https://apiv5.openrec.tv/api/v5/movies/" + video_id + "/chats"
        param = {
            "consented_chat_terms": False,
            "message": message,
            "quality_type": 2,
            "league_key": "",
            "to_user_id": ""
        }
        headers = self.HEADERS.copy()
        headers["uuid"] = self.__uuid
        headers["access-token"] = self.__access_token

        retval = 0
        j = {}
        try:
            j = requests.post(url, data=param, headers=headers, proxies=self.proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}

    def post_capture_reaction(self, capture_id: str, reaction: str) -> dict:
        """
            reactions:
                arara, bikkuri, gg, hatena, kakke, kami, kansya, kawaii, kusa, music, nice, odoroki, sugo, tsuyo, umai, wakuwaku, wara, yaba
        """
        url = "https://apiv5.openrec.tv/everyone/api/v5/reactions"
        param = {
            "target_id": capture_id,
            "target_type": "capture",
            "reaction_id": reaction
        }
        headers = self.HEADERS.copy()
        retval = 0
        j = {}

        if self.is_login:
            headers["uuid"] = self.__uuid
            headers["token"] = self.__token
            headers["random"] = self.__random
            try:
                j = requests.post(url, data=param, headers=headers, proxies=self.proxy).json()
            except (requests.exceptions.ConnectionError, ValueError):
                retval = -1

            return {"status": retval, "url": url, "data": j}

        else:
            with requests.Session() as s:
                r = s.post("https://www.openrec.tv/api-tv/user", headers=self.HEADERS, proxies=self.proxy)

                headers["uuid"] = r.cookies["uuid"]
                headers["token"] = r.cookies["token"]
                headers["random"] = r.cookies["random"]

                try:
                    j = s.post(url, data=param, headers=headers, proxies=self.proxy).json()
                except (requests.exceptions.ConnectionError, ValueError):
                    retval = -1

                return {"status": retval, "url": url, "data": j}


class Movie(Openrec):
    def __init__(self, movie_id, proxy=None):
        self.proxy = proxy
        self.movie_id = movie_id

    def info(self) -> dict:
        url = self.PUB_API + self.MOVIES_PATH + self.movie_id
        retval = 0
        j = {}
        try:
            j = requests.get(url, headers=self.HEADERS, proxies=self.proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}

    def comments(self, start_time: str):
        """
            start_time = "YYYY-MM-DDThh:mm:ss"
        """
        url = self.PUB_API + self.MOVIES_PATH + self.movie_id + "/chats"
        param = {
            "from_created_at": start_time,
            "is_including_system_message": "false"
        }
        retval = 0
        j = {}
        try:
            j = requests.get(url, headers=self.HEADERS, params=param, proxies=self.proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}

    def yell(self) -> dict:
        url = self.PUB_API + self.YELLLOG_PATH
        param = {
            "movie_id": self.movie_id,
        }
        try:
            j = requests.get(url, headers=self.HEADERS, params=param, proxies=self.proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}

    def capture(self) -> dict:
        url = self.PUB_API + self.CAPTURE_PATH
        param = {
            "movie_id": self.movie_id
        }
        try:
            j = requests.get(url, headers=self.HEADERS, params=param, proxies=self.proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}


class Capture(Openrec):
    def __init__(self, capture_id, proxy=None):
        self.proxy = proxy
        self.capture_id = capture_id

    def info(self) -> dict:
        url = self.PUB_API + self.CAPTURE_PATH + self.capture_id
        retval = 0
        j = {}
        try:
            j = requests.get(url, headers=self.HEADERS, proxies=self.proxy).json()
        except (requests.exceptions.ConnectionError, ValueError):
            retval = -1

        return {"status": retval, "url": url, "data": j}
