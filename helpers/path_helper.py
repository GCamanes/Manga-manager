from constants import Constants

class PathHelper:
    @staticmethod
    def get_manga_path(id: str) -> str:
        return f"{Constants.general.DL_PATH}/{id}/"
    
    @staticmethod
    def get_manga_json_path(id: str) -> str:
        return f"{PathHelper.get_manga_path(id)}{id}.json"
    
    @staticmethod
    def get_chapter_path(manga_id: str, chapter_number: str) -> str:
        return f"{PathHelper.get_manga_path(manga_id)}{chapter_number}/"
    
    @staticmethod
    def get_chapter_json_path(manga_id: str, chapter_number: str) -> str:
        return f"{PathHelper.get_chapter_path(manga_id, chapter_number)}{chapter_number}.json"