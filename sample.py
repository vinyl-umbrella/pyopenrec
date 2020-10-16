from pyopenrec import pyopenrec

movie = pyopenrec.Movie(movie_id="1o8q43q3yzk")
last_id = -1

while True:
    comments = movie.comments(start_time="2019-10-10T10:10:10")
    for comment in comments:
        if last_id == comment["id"]:
            continue
        print(comment["posted_at"], comment["user"]["id"], comment["message"])

    if len(comments) == 1 or comments[0]["posted_at"] == comments[-1]["posted_at"]:
        break

    last_id = comments[-1]["id"]
    start_time = comments[-1]["posted_at"][:-6]
