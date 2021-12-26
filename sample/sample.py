# import json
import pyopenrec


# login with email
user = pyopenrec.Openrec(email="YOUR_EMAIL", password="YOUR_PASSWORD")
# with open("./sample/secret.json", "r") as f:
#     cred = json.load(f)

# user = pyopenrec.Openrec(credentials=cred)
print("Login as {} ({})".format(user.name, user.id))

j = user.post_comment("n9ze3m2w184", "てすと")
if j["status"] == 200:
    print(j["data"])
else:
    print("Failed")
