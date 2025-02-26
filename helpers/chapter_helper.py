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
    
    @staticmethod
    def extract_chap_number_from_link(link):
        filter_text = ChapterHelper.get_matching_link(link)
        chapter_parts = link.split(filter_text)[-1].split("-")
        chapter_parts[0] = str(chapter_parts[0]).zfill(4)
        return ".".join(chapter_parts)