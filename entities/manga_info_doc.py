class MangaInfoDoc:
    """Represents a manga with its information and list of chapters."""
    def __init__(self, id: str , title: str , cover_path: str, authors: list[str], genres: list[str], status: str , chapters: list[str] = None):
        self.id: str  = id
        self.title: str  = title
        self.cover_path: str = cover_path
        self.authors: list[str] = authors
        self.genres: list[str] = genres
        self.status: str  = status
        self.chapters: list[str] = chapters

    def __repr__(self):
        return (f"#### Manga {self.title}\n* id={self.id}\n* cover={self.cover_path}\n* authors={self.authors}\n* genres={self.genres}\n"
                f"* status={self.status}\n* chapters({self.chapters})")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "cover_path": self.cover_path,
            "authors": self.authors,
            "genres": self.genres,
            "status": self.status,
            "chapters": self.chapters
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["title"],
            data["cover_path"],
            data["authors"],
            data["genres"],
            data["status"],
            data["chapters"]
        )