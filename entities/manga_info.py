
from entities.chapter_info import ChapterInfo


class MangaInfo:
    """Represents a manga with its information and list of chapters."""
    def __init__(self, id: str , title: str , coverLink: str, authors: list[str], genres: list[str], status: str , chapters: "list[ChapterInfo]" = None):
        self.id: str  = id
        self.title: str  = title
        self.coverLink: str = coverLink
        self.authors: list[str] = authors
        self.genres: list[str] = genres
        self.status: str  = status
        self.chapters: "list[ChapterInfo]" = chapters

    def __repr__(self):
        return (f"#### Manga {self.title}\n* id={self.id}\n* cover={self.coverLink}\n* authors={self.authors}\n* genres={self.genres}\n"
                f"* status={self.status}\n* chapters({len(self.chapters) if self.chapters != None else 0})")
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "coverLink": self.coverLink,
            "authors": self.authors,
            "genres": self.genres,
            "status": self.status,
            "chapters": [chapter.to_dict() for chapter in self.chapters]
        }

    @classmethod
    def from_dict(cls, data):
        chapters = [ChapterInfo.from_dict(chap) for chap in data.get("chapters", [])]
        return cls(
            data["id"],
            data["title"],
            data["coverLink"],
            data["authors"],
            data["genres"],
            data["status"],
            chapters
        )