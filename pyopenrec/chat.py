import json
import threading
import time
from typing import Callable, Optional, Union

import websocket

from .comment import Comment
from .util.enums import ChatType
from .video import Video


class ChatData:
    """
    Chat data from websocket.
    """

    type: int
    data: Union[Comment, dict]

    def __init__(self, type: int, data: Union[Comment, dict]):
        self.type = type
        self.data = data

    @property
    def type_name(self) -> str:
        try:
            return ChatType(self.type).name
        except ValueError:
            return "unknown"

    # example of data
    # info
    #   movie_id: int
    #   live_type: int
    #   onair_status: int # 1: onair 2: ?
    #   chat_id: int
    #   message: str # e.g. タイトルが圧倒的好評なPinapple on Pizzaやるぞ！！に変更されました。
    #   message_en: str # e.g. The title has been changed to 圧倒的好評なPinapple on Pizzaやるぞ！！.
    #   message_ko: str # e.g. 제목이 圧倒的好評なPinapple on Pizzaやるぞ！！로 변경되었습니다.
    #   message_zh: str # e.g. 标题已经更新成圧倒的好評なPinapple on Pizzaやるぞ！！'
    #   system_message: dict
    #     type: str # e.g. change_live_title
    #     style: int
    #     poll: ?
    #     user: ?
    #     fes_event: dict
    #     cre_dt: str # e.g. '2023-06-24 14:51:53'


class Chat:
    """
    Chat class.

    - `connect_chat(vid, debug, reconnect, on_open, on_message, on_error, on_close)`: connect to chat server
    """

    @staticmethod
    def __get_ws_url(vid: str) -> str:
        """
        Get the websocket url for the chat server.

        Args:
            vid (str): video id

        Returns:
            str: websocket url
        """
        mid = Video(vid).movie_id
        now = int(time.time())
        ws = f"wss://chat.openrec.tv/socket.io/?movieId={mid}&connectAt={now}&referrer=https%3A%2F%2Fwww.openrec.tv%2Flive%2F{vid}&isExcludeLiveViewers=true&EIO=3&transport=websocket"
        return ws

    @staticmethod
    def __parse_chat(msg: str) -> ChatData:
        """
        Parse chat data from websocket.

        Args:
            msg (str): received websocket message

        Returns:
            ChatData: parsed data
        """
        chat_type = None
        chat_data = {}
        index = msg.find("[")

        if index == -1:
            # ping
            chat_type = 100
            chat_data = msg
        elif index != 2:
            # system message
            chat_type = 101
            chat_data = msg
        else:
            message = msg[index:].strip('"\n ')
            j = json.loads(message)
            if j[0] != "message":
                chat_type = 102
                chat_data = message

            else:
                ws_data = json.loads(j[1])
                chat_type = ws_data["type"]
                chat_data = ws_data["data"]

        return ChatData(chat_type, chat_data)

    @staticmethod
    def connect_chat(
        vid: str,
        debug: bool = False,
        reconnect: Optional[bool] = False,
        on_open: Optional[Callable[[], None]] = None,
        on_message: Optional[Callable[[ChatData], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        on_close: Optional[Callable[[int, str], None]] = None,
    ):
        """
        connect to chat server.

        Args:
            vid (str): video id
            debug (bool): enable debug mode. default is False
            reconnect (bool): reconnect when connection is closed except streaming is finished
            on_open: callback function when connection is established
            on_message: callback function when message is received
            on_error: callback function when error occurs
            on_close: callback function when connection is closed
        """

        global EXIT_FLAG
        EXIT_FLAG = False

        def _send_ping(ws):
            ws.send("2")
            global ping_thread
            ping_thread = threading.Timer(interval=25, function=_send_ping, args=(ws,))
            ping_thread.start()

        def _on_o(_):
            if on_open:
                on_open()

        def _on_m(ws, message: str):
            if on_message:
                msg = Chat.__parse_chat(message)
                if msg.type_name == ChatType.stream_end.name:
                    global EXIT_FLAG
                    EXIT_FLAG = True
                    ws.close()
                elif msg.type_name == ChatType.chat.name and isinstance(msg.data, dict):
                    # if data is chat, parse data to Comment object
                    msg.data = Comment(comment_from_ws=msg.data)
                on_message(msg)

        def _on_e(_, err: Exception):
            if on_error:
                on_error(err)

        def _on_c(_, status: int, msg: str):
            if on_close:
                if status != 1006:
                    # if 1006, reconnect
                    # if status is not 1006, close connection
                    global EXIT_FLAG
                    EXIT_FLAG = True
                on_close(status, msg)

        url = Chat.__get_ws_url(vid)
        websocket.enableTrace(debug)

        while True:
            ws = websocket.WebSocketApp(
                url, on_open=_on_o, on_message=_on_m, on_error=_on_e, on_close=_on_c
            )

            global ping_thread
            ping_thread = threading.Timer(interval=25, function=_send_ping, args=(ws,))
            ping_thread.start()

            ws.run_forever()
            ping_thread.cancel()

            # if stream_end or close status is not 1006, break
            if EXIT_FLAG:
                break

            # if reconnect is False, break
            if not reconnect:
                break
