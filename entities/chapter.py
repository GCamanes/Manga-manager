from helpers.chapter_helper import ChapterHelper


class ChapterInfo:
    """Represents a manga chapter"""
    def __init__(self, link):
        self.number = ChapterHelper.extract_chap_number_from_link(link)
        self.link = link

    def __repr__(self):
        return f"Chapter(number={self.number}, url={self.link})"