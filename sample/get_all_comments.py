import time
from datetime import datetime

import pyopenrec


last_id = 0
dt = datetime(2020, 1, 1, 0, 0, 0)
vid = input("input video id: ")
video = pyopenrec.Openrec().Video(vid)

while True:
    comments = video.get_comments(dt, 100)
    # if got all comments, exit
    if comments[-1].id == last_id:
        break

    for comment in comments:
        if comment.id <= last_id:
            continue
        print(
            comment.posted_at,
            comment.user.nickname,
            comment.user.id,
            comment.message,
        )

    last_id = comments[-1].id
    dt = datetime.fromisoformat(comments[-1].posted_at)

    time.sleep(1)
