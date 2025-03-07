class ChapterPagesInfo:
    """Represents a manga chapter"""
    def __init__(self, manga_id: str, number: str, link: str, page_links: list[str] = []):
        self.manga_id: str = manga_id
        self.number: str = number
        self.link: str = link
        self.page_links: list[str] = page_links

    def __repr__(self):
        return f"Chapter from manga {self.manga_id} (number={self.number}, url={self.link}, pages={len(self.page_links)})"
    
    def to_dict(self) -> dict:
        return {
            "manga_id": self.manga_id,
            "number": self.number,
            "link": self.link,
            "page_links": self.page_links
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["manga_id"], data["number"], data["link"], data["page_links"])