# 連投 without login
import subprocess
import time
from multiprocessing import Pool

import pyopenrec

tor_proxy = {
    "http": "socks5://127.0.0.1:9050",
    "https": "socks5://127.0.0.1:9050",
}
vid = input("input stream id: ")


def post_template_comment(vid: str):
    # make no login user
    user = pyopenrec.Openrec(proxy=tor_proxy)
    print("logined")
    # post template message
    j = user.post_template_comment(vid, 0)
    print(j["status"])


while True:
    subprocess.run(["service", "tor", "restart"])
    time.sleep(5)

    p = Pool(5)
    for _ in range(10):
        p.apply_async(post_template_comment, args=(vid,))

    time.sleep(60)
