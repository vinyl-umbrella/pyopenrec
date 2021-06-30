import time
from pyopenrec import pyopenrec

movie = pyopenrec.Movie(movie_id="1o8q43q3yzk")
start_time = "2019-01-01T00:00:00"
last_id = -1

while True:
    comments = movie.comments(start_time)
    if comments["status"] != -1:
        for comment in comments["data"]:
            if last_id == comment["id"]:
                continue
            print(comment["posted_at"], comment["user"]["id"], comment["message"])

        if len(comments["data"]) == 1 or comments["data"][0]["posted_at"] == comments["data"][-1]["posted_at"]:
            break

    time.sleep(1)

    last_id = comments["data"][-1]["id"]
    start_time = comments["data"][-1]["posted_at"][:-6]
