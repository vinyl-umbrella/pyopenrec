class Config:
    PUB_API = "https://public.openrec.tv/external/api/v5"

    MOVIES_PATH = "/movies/"
    YELLLOG_PATH = "/yell-logs/"
    CAPTURE_PATH = "/captures/"
    CAPTURERANK_PATH = "/capture-ranks/"
    CHANNEL_PATH = "/channels/"

    HEADERS = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"
    }
