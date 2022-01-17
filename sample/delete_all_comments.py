import time
from datetime import datetime

import pyopenrec

# login
user = pyopenrec.Openrec(email="YOUR_EMAIL", password="YOUR_PASSWORD")
print(f"Login as {user.name} ({user.id})")

last_id = 0
dt = datetime(2021, 12, 1, 0, 0, 0)
vid = input("input video id: ")

while True:
    comments = user.get_comment(vid, dt, 100)
    # if got all comments, exit
    if comments["data"][-1]["id"] == last_id:
        break

    for comment in comments["data"]:
        if comment["id"] <= last_id:
            continue
        # delete your comment
        elif comment["user"]["id"] == user.id:
            print("DELETE", comment["user"]["nickname"], comment["message"])
            res = user.delete_comment(vid, str(comment["id"]))

    last_id = comments["data"][-1]["id"]
    dt = datetime.fromisoformat(comments["data"][-1]["posted_at"])

    time.sleep(1)
