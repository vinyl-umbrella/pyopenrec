# 連投 without login
import pyopenrec

vid = input("input stream id: ")

for _ in 10:
    # make no login user
    user = pyopenrec.Openrec()
    # post template message
    user.post_template_comment(vid, 1)
