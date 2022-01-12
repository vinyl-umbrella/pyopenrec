import threading
import time

import pyopenrec
from pyopenrec.chat import Chat

import websocket


def send_ping(ws):
    while True:
        time.sleep(25)
        ws.send("2")


def on_m(_, message: str):
    msg = Chat.chat_parser(message)
    if msg.type == "vote_start":
        print("[vote start]")
        print("title", msg.data["title"])
        vote_id = msg.data["id"]

        for alt in msg.data["votes"]:
            print(alt["index"], ":", alt["text"], end=", ")
        print()

        index = input("Your choise: ")
        # post 5 times as non login user
        for _ in range(5):
            user = pyopenrec.Openrec()
            user.post_vote(vid, vote_id, index)
    # elif msg.type == "vote_progress":
    #     print(msg.data)
    elif msg.type == "vote_end":
        for alt in msg.data["votes"]:
            print(alt["text"], "count:", alt["count"],
                  "ratio:", alt["ratio"], "rank:", alt["rank"])


def on_e(_, err):
    print("[err]", err)


def on_c(_, status, msg):
    print("[close]", status, msg)


def on_o(_):
    print("[open]")


if __name__ == "__main__":
    vid = input("vid: ")
    uri = Chat.get_ws(vid)
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(uri,
                                on_open=on_o,
                                on_message=on_m,
                                on_error=on_e,
                                on_close=on_c)

    th = threading.Thread(target=send_ping, args=(ws,))
    th.start()

    ws.run_forever()
