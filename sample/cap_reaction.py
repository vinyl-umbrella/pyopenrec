# increase capture reaction
from pyopenrec import Openrec, ReactionType

cap_id = input("input capture id: ")

client = Openrec(email="YOUR_EMAIL", password="YOUR_PASSWORD")
capture = client.Capture(cap_id)
print(capture.id, capture.title)

capture.post_reaction(ReactionType.kawaii)
