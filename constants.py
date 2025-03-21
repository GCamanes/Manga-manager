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
        CHAPTER_CUSTOMS_JSON = "chapter_customs.json"
        
    class firebase:
        service_account_key = "ServiceAccountKey.json"
        mangas_collection = "mangas"
        chapters_collection = "chapters"
        
    class chapter:
        FILTERS = ["ch-", "chapter-"]
        CLASSIC_REGEXP = r'.*(-ch-|-chapter-|-punch-)(\d+)(?:-?v?(\d+))?.*$'
        CUSTOM_REGEXP = r'(\d+)(?:-?v?(\d+))?.*$'