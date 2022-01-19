import json
from os import path

import pyopenrec
from pyopenrec.chat import ChatData


VID = input("Video id: ")
credentials = "./secret.json"
if path.isfile(credentials):
    with open("./secret.json", "r") as f:
        cred = json.load(f)
    OPENREC = pyopenrec.Openrec(credentials=cred)
else:
    OPENREC = pyopenrec.Openrec(email="YOUR_EMAIL", password="YOUR_PASSWORD")
    with open(credentials, "w") as f:
        json.dump(OPENREC._credentials, f, ensure_ascii=False, indent=4)


def on_m(msg: ChatData):
    if msg.type == "chat" and msg.data["user_key"] != OPENREC.id:
        # mute検知
        if msg.data["is_muted"]:
            pass

        # chat command
        if msg.data["message"].startswith("@bot "):
            command = msg.data["message"].split(" ")
            if command[1] == "bot_command":
                OPENREC.post_comment(VID, "bot response")
                pass

    # 同時接続数
    elif msg.type == "live_viewers":
        pass

    # 配信開始
    elif msg.type == "stream_start":
        pass

    # 配信終了
    elif msg.type == "stream_end":
        pass

    # ban
    elif msg.type == "ban":
        pass

    # ban解除
    elif msg.type == "unban":
        pass

    # staff追加
    elif msg.type == "add_staff":
        pass

    # staff削除
    elif msg.type == "remove_staff":
        pass

    # タイトル変更など
    elif msg.type == "info":
        pass

    # テロップ更新
    elif msg.type == "telop":
        pass

    # サブスク入会
    elif msg.type == "subscription":
        pass

    # アンケート開始
    elif msg.type == "vote_start":
        pass

    # アンケート途中結果
    elif msg.type == "vote_progress":
        pass

    # アンケート終了、結果
    elif msg.type == "vote_end":
        pass


def on_e(err):
    print("[err]", err)


def on_c(status, msg):
    print("[close]", status, msg)


def on_o():
    pass


if __name__ == "__main__":
    OPENREC.connect_chat(VID, on_open=on_o, on_message=on_m, on_error=on_e, on_close=on_c)
