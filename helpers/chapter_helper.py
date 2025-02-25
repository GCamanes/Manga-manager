import re
from bs4 import BeautifulSoup
import requests
from constants import Constants
from entities.manga_info import MangaInfo

class ChapterHelper:
    @staticmethod
    def get_matching_link(link):
        for filter_text in Constants.chapter.FILTERS:
            if filter_text in link:
                return filter_text
        return None