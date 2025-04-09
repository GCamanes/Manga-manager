
import re
from entities.download.chapter_info import ChapterInfo
from helpers.string_helper import StringHelper


class MangaInfo:
    """Represents a manga with its information and list of chapters."""
    def __init__(self, id: str , firebase_id: str, title: str , cover_path: str, authors: list[str], genres: list[str], status: str , chapters: "list[ChapterInfo]" = None):
        self.id: str  = id
        self.firebase_id: str = firebase_id
        self.title: str  = title
        self.cover_path: str = cover_path
        self.authors: list[str] = authors
        self.genres: list[str] = genres
        self.status: str  = status
        self.chapters: "list[ChapterInfo]" = chapters

    def __repr__(self):
        return (f"#### Manga {self.title}\n* id={self.id}\n* firebase_id={self.firebase_id}\n* cover={self.cover_path}\n* authors={self.authors}\n* genres={self.genres}\n"
                f"* status={self.status}\n* chapters({len(self.chapters) if self.chapters != None else 0})")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "firebase_id": self.firebase_id,
            "title": self.title,
            "cover_path": self.cover_path,
            "authors": self.authors,
            "genres": self.genres,
            "status": self.status,
            "chapters": [chapter.to_dict() for chapter in self.chapters]
        }

    def to_dict_without_link(self) -> dict:
        return {
            "id": self.id,
            "firebase_id": self.firebase_id,
            "title": self.title,
            "cover_path": self.cover_path,
            "authors": self.authors,
            "genres": self.genres,
            "status": self.status,
            "chapters": [chapter.number for chapter in self.chapters]
        }

    @classmethod
    def from_dict(cls, data):
        chapters = [ChapterInfo.from_dict(chap) for chap in data.get("chapters", [])]
        return cls(
            data["id"],
            data["firebase_id"],
            data["title"],
            data["cover_path"],
            data["authors"],
            data["genres"],
            data["status"],
            chapters
        )