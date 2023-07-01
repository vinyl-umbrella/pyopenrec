from os import path

from pyopenrec import ChatType, Openrec
from pyopenrec.chat import ChatData
from pyopenrec import credentials

VID = input("Video ID: ")
CLIENT = None
COMMAND_PREFIX = "@bot"


def on_o():
    pass


def on_m(msg: ChatData):
    if msg.type_name == ChatType.chat.name and msg.data.user.id != CLIENT.me().id:
        # mute検知
        if msg.data.is_muted:
            return

        # chat
        if msg.data.message.startswith(COMMAND_PREFIX):
            command = msg.data.message[len(COMMAND_PREFIX) + 1 :]
            if command == "BOT_COMMAND":
                CLIENT.Video(VID).post_comment("bot response")
                return

    # 同時接続数
    if msg.type_name == ChatType.live_viewers:
        return

    # 配信開始
    if msg.type_name == ChatType.stream_start:
        return

    # 配信終了
    if msg.type_name == ChatType.stream_end:
        return

    # ban
    if msg.type_name == ChatType.ban:
        return

    # ban解除
    if msg.type_name == ChatType.unban:
        return

    # staff追加
    if msg.type_name == ChatType.staff_add:
        return

    # staff削除
    if msg.type_name == ChatType.remove_staff:
        return

    # タイトル変更など
    if msg.type_name == ChatType.info:
        return

    # テロップ
    if msg.type_name == ChatType.telop:
        return

    # サブスク入会
    if msg.type_name == ChatType.subscription:
        return

    # アンケ開始
    if msg.type_name == ChatType.vote_start:
        return

    # アンケ途中結果
    if msg.type_name == ChatType.vote_progress:
        return

    # アンケ終了
    if msg.type_name == ChatType.vote_end:
        return

    # 拡張機能
    if msg.type_name == ChatType.extention:
        return

    # 未解析のデータ
    if msg.type_name == ChatType.unknown:
        return


def on_e(e):
    print("error", e)


def on_c(status, reason):
    print("close", status, reason)


if __name__ == "__main__":
    secret = "./secret.json"

    if path.isfile(secret):
        with open(secret, "r") as f:
            cred = credentials.OpenrecCredentials()
            cred.load(f.read())

        CLIENT = Openrec(credentials=cred)
        print(CLIENT.me().id)

    else:
        CLIENT = Openrec(email="YOUR_EMAIL", password="YOUR_PASSWORD")
        with open(secret, "w") as f:
            f.write(str(CLIENT.credentials))

    CLIENT.Chat().connect_chat(
        VID,
        debug=False,
        reconnect=True,
        on_open=on_o,
        on_message=on_m,
        on_close=on_c,
        on_error=on_e,
    )
