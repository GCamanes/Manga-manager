# constants.py
# File containing organized constants

class Constants:
    class general:
        WEBSITE = "https://mangapark.io"
        TITLE_PATH = "title"
        BASE_TITLE_URL = f"{WEBSITE}/{TITLE_PATH}/"
        DL_PATH = ".manga"
        MANGA_IDS_JSON = "manga_list.json"
        CHAPTER_PATTERNS_JSON = "chapter_patterns.json"
        
    class firebase:
        service_account_key = "ServiceAccountKey.json"
        mangas_collection = "mangas"
        
    class chapter:
        FILTERS = ["ch-", "chapter-"]