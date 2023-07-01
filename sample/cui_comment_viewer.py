from pyopenrec import ChatType, Openrec
from pyopenrec.chat import ChatData


def on_o():
    pass


def on_m(msg: ChatData):
    if msg.type_name in [
        ChatType.check_need_refresh.name,
        ChatType.live_viewers.name,
        ChatType.system_msg.name,
        ChatType.ping.name,
    ]:
        pass
    elif msg.type_name == ChatType.chat.name:
        if msg.data.stamp:
            # if stamp
            print(
                f"{msg.data.user.nickname}({msg.data.user.id})\t{msg.data.stamp['image_url']}"
            )
        else:
            print(f"{msg.data.user.nickname}({msg.data.user.id})\t{msg.data.message}")

    else:
        print(msg.type, msg.type_name)
        print(msg.data)


def on_e(e):
    print("error", e)


def on_c(status, reason):
    print("close", status, reason)


Openrec.Chat().connect_chat(
    "indegnasen",
    debug=False,
    reconnect=True,
    on_open=on_o,
    on_message=on_m,
    on_close=on_c,
    on_error=on_e,
)
