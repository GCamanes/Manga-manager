# constants.py
# File containing organized constants

class Constants:
    class general:
        WEBSITE = f"https://mangapark.io"
        TITLE_PATH = f"title"
        BASE_TITLE_URL = f"{WEBSITE}/{TITLE_PATH}/"
        DL_PATH = ".manga"
        
    class firebase:
        fb_account_file = "ServiceAccountKey.json"
        
    class chapter:
        FILTERS = ["ch-", "chapter-"]