from entities.firebase.manga_doc import MangaDoc

class MangaDocLight:
    """Represents a manga with its information and list of chapters."""
    def __init__(self, id: str , title: str , cover_path: str, authors: list[str], genres: list[str], status: str , last_chapter: str = None):
        self.id: str  = id
        self.title: str  = title
        self.cover_path: str = cover_path
        self.authors: list[str] = authors
        self.genres: list[str] = genres
        self.status: str  = status
        self.last_chapter: str = last_chapter
        
    @classmethod
    def from_other(cls, other: "MangaDoc", chapter: str):
        return cls(
            id=other.id,
            title = other.title,
            cover_path = other.cover_path,
            authors = other.authors,
            genres = other.genres,
            status = other.status,
            last_chapter = chapter,
        )

    def __repr__(self):
        return (f"#### Manga doc {self.title}\n* id={self.id}\n* cover={self.cover_path}\n* authors={self.authors}\n* genres={self.genres}\n"
                f"* status={self.status}\n* last_chapter({self.last_chapter})")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "cover_path": self.cover_path,
            "authors": self.authors,
            "genres": self.genres,
            "status": self.status,
            "last_chapter": self.last_chapter
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
            data["last_chapter"]
        )