import json
import pyopenrec

j = pyopenrec.get_video_info("1o8q43q3yzk")

with open("test.json", "w") as f:
    json.dump(j, f, indent=2, ensure_ascii=False)
