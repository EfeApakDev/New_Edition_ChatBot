import os


class Config():
    # Get these values from my.telegram.org
    # https://my.telegram.org
    BOT_ID = int(os.environ.get("BOT_ID"))
    OWNER_ID = int(os.environ.get("OWNER_ID"))
