from helpers.chapter_helper import ChapterHelper

class ChapterInfo:
    """Represents a manga chapter"""
    def __init__(self, link: str):
        self.number: str = ChapterHelper.extract_chap_number_from_link(link)
        self.link: str = link

    def __repr__(self):
        return f"Chapter(number={self.number}, url={self.link})"