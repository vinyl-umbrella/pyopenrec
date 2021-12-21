from datetime import datetime
import pyopenrec
import time


last_id = 0
dt = datetime(2015, 1, 1, 0, 0, 0)
vid = input("input video id: ")

while True:
    comments = pyopenrec.get_comment(vid, dt, 5)
    # if got all comments, exit
    if comments["data"][-1]["id"] == last_id:
        break

    for comment in comments["data"]:
        if comment["id"] <= last_id:
            continue
        print(comment["id"], comment["posted_at"],
              comment["user"]["id"], comment["user"]["nickname"], comment["message"])

    last_id = comments["data"][-1]["id"]
    dt = datetime.fromisoformat(comments["data"][-1]["posted_at"])

    time.sleep(1)
