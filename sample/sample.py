import json
import pyopenrec


# login with email
# user = pyopenrec.Openrec(email="YOUR_EMAIL", password="YOUR_PASSWORD")
# j = user.timeline(2)

# without login
user = pyopenrec.Openrec()
j = user.post_capture_reaction("l9nk1xwegd1", "kawaii")

with open("test.json", "w") as f:
    json.dump(j, f, indent=2, ensure_ascii=False)
