# constants.py
# File containing organized constants

class Constants:
    class general:
        WEBSITE = f"https://mangapark.io"
        TITLE_PATH = f"title"
        BASE_TITLE_URL = f"{WEBSITE}/{TITLE_PATH}/"
        DL_PATH = ".manga"
        
    class firebase:
        service_account_key = "ServiceAccountKey.json"
        mangas_collection = "mangas"
        
    class chapter:
        FILTERS = ["ch-", "chapter-"]