import re

class MangaInfo:
    """Represents a manga with its information and list of chapters."""
    def __init__(self, id, title, authors, genres, status, chapters = []):
        self.id = id
        self.title = title
        self.authors = authors
        self.genres = genres
        self.status = status
        self.chapters = chapters

    def __repr__(self):
        return (f"#### Manga {self.title}\n* id={self.id}\n* authors={self.authors}\n* genres={self.genres}\n"
                f"* status={self.status}\n* chapters({len(self.chapters)})")