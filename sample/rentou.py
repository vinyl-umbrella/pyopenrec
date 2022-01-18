# 連投 without login
from copy import deepcopy

import pyopenrec

vid = input("input stream id: ")

for _ in range(3):
    # make no login user
    user = pyopenrec.Openrec()
    copied_user = deepcopy(user)
    # post template message
    copied_user.post_template_comment(vid, 1)
