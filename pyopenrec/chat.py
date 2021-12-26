import json
import time
from .video import Video
from .util.config import AUTHORIZED_API
from .util import http


class ChatData():
    """
    type: or
    data: {

    }
    """
    type = ""
    data = {}


class Chat:
    """
    - Change name color. Premium account only. Login Required.
    - Get chat URI.
    - Parse chat data from websocket.
    """
    is_login = False
    _credentials = None

    def update_name_color(self, color: str) -> dict:
        """
        Change name color. Premium account only. Login Required.
        param: hex color code (e.g. #201E2F)
        """
        if not self.is_login:
            raise Exception("Login Required.")

        url = AUTHORIZED_API + "/users/me/chat-setting"
        params = {"name_color": color}
        return http.request("PUT", url, params, self._credentials, proxy=self._proxy)

    @staticmethod
    def get_ws(vid: str) -> str:
        """
        Get chat URI.

        param
        -----
        vid: video id
        """
        v = Video()
        data = v.video_info(vid)
        mid = data["data"]["movie_id"]
        now = int(time.time())
        ws = "wss://chat.openrec.tv/socket.io/?movieId={}&connectAt={}&isExcludeLiveViewers=false&EIO=3&transport=websocket".format(
            mid, now)
        return ws

    @staticmethod
    def chat_parser(msg: str) -> ChatData:
        """
        Parse chat data from websocket.

        param
        -----
        msg: received websocket message
        """
        ret_data = ChatData()

        index = msg.find("[")
        if index == -1:
            ret_data.type = "ping"
            ret_data.data = msg
        elif index != 2:
            ret_data.type = "system_msg"
            ret_data.data = msg
        else:
            message = msg[index:].replace(
                "\\", "").replace('"{', "{").replace('}"', "}")
            j = json.loads(message)
            if j[0] != "message":
                ret_data.type = "unknown"
                ret_data.data = message

            else:
                t = j[1]["type"]
                ret_data.data = j[1]["data"]

                if t == 0:
                    ret_data.type = "chat"
                elif t == 1:
                    ret_data.type = "live_viewers"
                elif t == 3:
                    ret_data.type = "stream_end"
                elif t == 5:
                    ret_data.type = "stream_start"
                elif t == 6:
                    ret_data.type = "ban"
                elif t == 7:
                    ret_data.type = "unban"
                elif t == 8:
                    ret_data.type = "add_staff"
                elif t == 9:
                    ret_data.type = "remove_staff"
                elif t == 10:
                    ret_data.type = "need_refresh"
                elif t == 11:
                    ret_data.type = "info"
                elif t in [12, 13, 15]:
                    ret_data.type = "telop"
                elif t == 27:
                    ret_data.type = "subscription"
                elif t == 29:
                    ret_data.type = "vote_start"
                elif t == 30:
                    ret_data.type = "vote_progress"
                elif t == 31:
                    ret_data.type = "vote_end"

                else:
                    print(j[1])

        return ret_data
