import time
from datetime import datetime

from pyopenrec.comment import Comment


last_id = 0
dt = datetime(2020, 1, 1, 0, 0, 0)
vid = input("input video id: ")
c = Comment()

while True:
    comments = c.get_comment(vid, dt, 100)
    # if got all comments, exit
    if comments.data[-1]["id"] == last_id:
        break

    for comment in comments.data:
        if comment["id"] <= last_id:
            continue
        print(comment["posted_at"], comment["user"]["nickname"],
              comment["user"]["id"], comment["message"])

    last_id = comments.data[-1]["id"]
    dt = datetime.fromisoformat(comments.data[-1]["posted_at"])

    time.sleep(1)
