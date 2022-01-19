from pyopenrec.chat import Chat, ChatData


def on_m(msg: ChatData):
    comment_format = "{dt}  {username}({userid})  {m}"
    if msg.type == "chat":
        print(comment_format.format(
            dt=msg.data["message_dt"],
            username=msg.data["user_name"],
            userid=msg.data["user_key"],
            m=msg.data["message"]
        ))
    elif msg.type in ["live_viewers", "need_refresh", "ping"]:
        pass
    else:
        print(msg.type, msg.data)


Chat.connect_chat("n9ze3m2w184", on_message=on_m)
