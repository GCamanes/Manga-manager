from typing import Dict, List

class ChapterCustomsEntry:
    def __init__(self, black_list: List[str], chapter_fix: Dict[str, str]):
        self.black_list = black_list
        self.chapter_fix = chapter_fix

    def __repr__(self):
        return f"ChapterCustomsEntry(black_list={self.black_list}, chapter_fix={self.chapter_fix})"
    
    def get_entry(self, chapter_key: str) -> str | None :
        return self.chapter_fix.get(chapter_key, None)


class ChapterCustoms:
    def __init__(self, manga_data: Dict[str, Dict]):
        self.manga_entries = {
            key: ChapterCustomsEntry(value.get("black_list", []), value.get("chapter_fix", {}))
            for key, value in manga_data.items()
        }

    def __repr__(self):
        return f"ChapterCustoms(entries={self.manga_entries})"

    def get_entry(self, manga_key: str) -> ChapterCustomsEntry:
        return self.manga_entries.get(manga_key, None)