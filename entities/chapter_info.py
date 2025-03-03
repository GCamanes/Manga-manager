class ChapterInfo:
    """Represents a manga chapter"""
    def __init__(self, number: str, link: str):
        self.number: str = number
        self.link: str = link

    def __repr__(self):
        return f"Chapter(number={self.number}, url={self.link})"
    
    def to_dict(self):
        return {
            "number": self.number,
            "link": self.link
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["number"], data["link"])