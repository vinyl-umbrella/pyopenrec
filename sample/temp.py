from os import path
from pyopenrec import Openrec, credentials


# u = Openrec("finnegan330.2@gmail.com", "Lg8GLY99ZisxT9A").me()

secret = "./secret.json"

if path.isfile(secret):
    with open(secret, "r") as f:
        print()
        cred = credentials.OpenrecCredentials()
        cred.load(f.read())
        print(cred)

    # exit()
    CLIENT = Openrec(credentials=cred)
    print(CLIENT.me().id)
    for u in CLIENT.Info().stream_rank():
        print(u.title)
