import re

class MangaInfo:
    """Represents a manga with its information and list of chapters."""
    def __init__(self, id, title, authors, genres, status, chapters = []):
        self.id = id,
        self.title = title
        self.authors = authors
        self.genres = genres
        self.status = status
        self.chapters = chapters

    def __repr__(self):
        return (f"Manga(title={self.title}, id={self.id}, authors={self.authors}, genres={self.genres}, "
                f"status={self.status}"
                f"chapters({len(self.chapters)})")