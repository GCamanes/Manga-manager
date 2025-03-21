class ChapterDoc:
    """Represents a manga chapter doc"""
    def __init__(self, number: str, pages: list[str]):
        self.number: str = number
        self.pages: str = pages

    def __repr__(self):
        return f"Chapter doc {self.number} ({self.pages})"
    
    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "pages": self.pages
        }