import json
import threading
import time

import websocket

from .util import http
from .util.config import AUTHORIZED_API
from .video import Video


class ChatData():
    """
    type: "chat" || "live_viewers" || "stream_end" || "stream_start" || "ban" || "unban" || "add_staff" || "remove_staff" || "need_refresh" || "info" || "telop" || "subscription" || "vote_start" || "vote_progress" || "vote_end" || "unknown"
    data: {}
    """
    type: str
    data: dict


class Chat:
    """
    - Change name color. Premium account only. Login Required.
    - Get chat URI.
    - Parse chat data from websocket.
    - Connect chat.
    """
    is_login = False
    _credentials = None
    _proxy = {}

    def update_name_color(self, color: str) -> http.Response:
        """
        Change name color. Premium account only. Login Required.
        param: hex color code (e.g. #201E2F)
        """
        if not self.is_login:
            raise Exception("Login Required.")

        url = f"{AUTHORIZED_API}/users/me/chat-setting"
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
        mid = data.data["movie_id"]
        now = int(time.time())
        ws = f"wss://chat.openrec.tv/socket.io/?movieId={mid}&connectAt={now}&isExcludeLiveViewers=false&EIO=3&transport=websocket"
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
            message = msg[index:].strip('"\n ')
            j = json.loads(message)
            if j[0] != "message":
                ret_data.type = "unknown"
                ret_data.data = message

            else:
                ws_data = json.loads(j[1])
                t = ws_data["type"]
                ret_data.data = ws_data["data"]

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
                    ret_data.type = "unknown"

        return ret_data

    @staticmethod
    def connect_chat(vid: str, on_open=None, on_message=None, on_error=None, on_close=None):
        """
        connect chat

        param
        -----
        vid: video id
        on_open: Run on connect to chat server.
            function()
        on_message: Run on message arrived.
            function(msg: pyopenrec.chat.ChatData)
        on_error: Run on error.
            function(status, msg)
        on_close: Run on close websocket.
            function(err)
        """
        def _send_ping(ws: websocket.WebSocketApp):
            while True:
                time.sleep(25)
                ws.send("2")

        def _on_m(_, message):
            if on_message:
                msg = Chat.chat_parser(message)
                on_message(msg)

        def _on_o(_):
            if on_open:
                on_open()

        def _on_c(_, status, msg):
            if on_close:
                on_close(status, msg)

        def _on_e(_, err):
            if on_error:
                on_error(err)

        url = Chat.get_ws(vid)
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(url,
                                    on_open=_on_o,
                                    on_message=_on_m,
                                    on_error=_on_e,
                                    on_close=_on_c
                                    )

        th = threading.Thread(target=_send_ping, args=(ws,))
        th.start()
        ws.run_forever()
