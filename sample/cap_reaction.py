# increase capture reaction
import pyopenrec

cap_id = input("input capture id: ")

for _ in 10:
    # make no login user
    user = pyopenrec.Openrec()
    # post reaction
    user.post_capture_reaction(cap_id, "kawaii")
