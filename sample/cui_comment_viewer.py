from pyopenrec.chat import Chat
import threading
import time
import websocket


def send_ping(ws):
    while True:
        time.sleep(25)
        ws.send("2")


def on_m(_, message: str):
    msg = Chat.chat_parser(message)
    comment_format = "{dt}  {username}({userid})  {m}"
    if msg.type == "chat":
        print(comment_format.format(
            dt=msg.data["message_dt"],
            username=msg.data["user_name"],
            userid=msg.data["user_key"],
            m=msg.data["message"]
        ))


def on_e(_, err):
    print("[err]", err)


def on_c(_):
    print("[close]")


def on_o(_):
    print("[open]")


if __name__ == "__main__":
    uri = Chat.get_ws("n9ze3m2w184")
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(uri,
                                on_open=on_o,
                                on_message=on_m,
                                on_error=on_e,
                                on_close=on_c)

    th = threading.Thread(target=send_ping, args=(ws,))
    th.start()

    ws.run_forever()
