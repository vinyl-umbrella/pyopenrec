import json
import pyopenrec


# # login
credentials = pyopenrec.login(email="YOUR_EMAIL", password="YOUR_PASSWORD")
# print(credentials["data"])

# me
# j = pyopenrec.me(credentials['data'])
j = pyopenrec.timeline(2, credentials['data'])

with open("test.json", "w") as f:
    json.dump(j, f, indent=2, ensure_ascii=False)
