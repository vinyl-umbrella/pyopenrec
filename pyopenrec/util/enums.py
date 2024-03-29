from enum import Enum


class ChatType(Enum):
    chat = 0
    live_viewers = 1
    stream_end = 3
    stream_start = 5
    ban = 6
    unban = 7
    add_staff = 8
    remove_staff = 9
    check_need_refresh = 10
    info = 11
    set_telop = 12
    delete_telop = 13
    # telop = 14
    telop = 15
    subscription = 27
    vote_start = 29
    vote_progress = 30
    vote_end = 31
    extention = 43
    # ---
    ping = 100
    system_msg = 101
    unknown = 102


class VideoType(Enum):
    coming_up = 0
    live = 1
    vod = 2


class ReactionType(Enum):
    kawaii = "kawaii"
    kakke = "kakke"
    music = "music"
    namida = "namida"
    netabare = "netabare"
    gg = "gg"
    wakuwaku = "wakuwaku"
    kansya = "kansya"
    bikkuri = "bikkuri"
    hatena = "hatena"
    kusa = "kusa"
    wara = "wara"
    sugo = "sugo"
    umai = "umai"
    nice = "nice"
    tsuyo = "tsuyo"
    kami = "kami"
    odoroki = "odoroki"
    yaba = "yaba"
    arara = "arara"
