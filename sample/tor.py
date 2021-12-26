import pyopenrec


tor_proxy = {
    "http": "socks5://127.0.0.1:9050",
    "https": "socks5://127.0.0.1:9050",
}

cap_id = input("input capture id: ")

for _ in range(3):
    # make no login user through tor
    user = pyopenrec.Openrec(proxy=tor_proxy)
    # post reaction
    j = user.post_capture_reaction(cap_id, "kawaii")
    if j["data"]:
        print(j["data"])
