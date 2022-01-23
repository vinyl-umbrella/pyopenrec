import subprocess
import time
from multiprocessing import Pool

import pyopenrec


tor_proxy = {
    "http": "socks5://127.0.0.1:9050",
    "https": "socks5://127.0.0.1:9050",
}
cap_id = input("input capture id: ")


def post_reaction(cap_id: str):
    # make no login user through tor
    user = pyopenrec.Openrec(proxy=tor_proxy)
    print("logined")
    # post reaction
    j = user.post_capture_reaction(cap_id, "kawaii")
    print(j["status"])


while True:
    subprocess.run(["sudo", "-p", "database", "service", "tor", "restart"])
    time.sleep(5)

    p = Pool(4)
    for _ in range(20):
        p.apply_async(post_reaction, args=(cap_id,))

    time.sleep(60)
