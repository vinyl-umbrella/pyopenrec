import json
import pyopenrec


# # login
# credentials = pyopenrec.login(email="YOUR_EMAIL", password="YOUR_PASSWORD")
# print(credentials["data"])

# # video
# j = pyopenrec.get_stream_list()
# j = pyopenrec.get_vod_list(page=2)
# j = pyopenrec.get_movie_list(sort="-total_yells")
j = pyopenrec.get_video_info("1o8q43q3yzk")
# j = pyopenrec.get_video_detail("1o8q43q3yzk", credentials['data'])

# # comment
# j = pyopenrec.get_comment("n9ze3m2w184", "2021-12-18T17:30:33+09:00")
# j = pyopenrec.get_recent_comment("n9ze3m2w184")
# j = pyopenrec.get_vod_comment("e2zw69jmw8o")
# j = pyopenrec.post_comment("kdr7x6y5w8j", "test", credentials["data"])
# j = pyopenrec.post_vod_comment("n9ze3n30184", "test", credentials["data"])
# j = pyopenrec.reply_vod_comment("e2zw69jmw8o", 140103, "test", credentials["data"])


with open("test.json", "w") as f:
    json.dump(j, f, indent=2, ensure_ascii=False)
