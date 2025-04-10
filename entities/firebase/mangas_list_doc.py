from typing import List, Optional
from entities.firebase.manga_doc_light import MangaDocLight

class MangasListDoc:
    """Represents a manga with its information and list of chapters."""
    def __init__(self, mangas: Optional[List[MangaDocLight]] = None):
        self.mangas: List[MangaDocLight] = mangas or []

    def __repr__(self):
        return (f"#### Mangas {self.mangas}")

    def to_dict(self) -> dict:
        return {
            "mangas": [manga.to_dict() for manga in self.mangas]
        }

    @classmethod
    def from_dict(cls, data):
        mangas = [MangaDocLight.from_dict(manga) for manga in data.get("mangas", [])]
        return cls(mangas)
        
    def add_or_replace(self, new_manga: MangaDocLight):
        for i, manga in enumerate(self.mangas):
            if manga.id == new_manga.id:
                self.mangas[i] = new_manga
                break
        else:
            self.mangas.append(new_manga)

        self.mangas.sort(key=lambda m: m.id)
        
    def remove_if_present(self, manga_id: str):
        self.mangas = [
            manga for manga in self.mangas if manga.id != manga_id
        ]