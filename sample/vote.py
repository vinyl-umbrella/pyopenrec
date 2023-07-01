from pyopenrec import Openrec, ChatType
from pyopenrec.chat import ChatData


def on_m(msg: ChatData):
    if msg.type_name == ChatType.vote_start.name:
        print("[vote start]")
        print("title", msg.data["title"])
        vote_id = msg.data["id"]

        for alt in msg.data["votes"]:
            print(alt["index"], ":", alt["text"], end=", ")
        print()

        index = input("Your choise: ")
        CLIENT.Video(vid).post_vote(vote_id, index)

    elif msg.type_name == ChatType.vote_progress.name:
        print(msg.data)

    elif msg.type_name == ChatType.vote_end.name:
        for alt in msg.data["votes"]:
            print(
                alt["text"],
                "count:",
                alt["count"],
                "ratio:",
                alt["ratio"],
                "rank:",
                alt["rank"],
            )


def on_e(err):
    print("[err]", err)


CLIENT = Openrec(email="YOUR_EMAIL", password="YOUR_PASSWORD")
vid = input("video id: ")
CLIENT.Chat().connect_chat(vid, reconnect=True, on_message=on_m, on_error=on_e)
