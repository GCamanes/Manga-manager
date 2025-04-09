import argparse
import os
import shutil
import sys
from constants import Constants
from entities.chapter_patterns import ChapterPatterns
from entities.manga_list import MangaList
from helpers.chapter_helper import ChapterHelper
from helpers.file_helper import FileHelper
from helpers.manga_helper import MangaHelper
from helpers.path_helper import PathHelper

def get_manga_ids() -> MangaList:
    return FileHelper.load_json_file(Constants.general.MANGA_IDS_JSON, MangaList.from_dict, allow_missing=True)

def download_manga(manga_id: str, need_to_add: bool = False) -> None:
    print(f"\n# Downloading {manga_id} ...")
    if need_to_add:
        manga_list = FileHelper.load_json_file(Constants.general.MANGA_IDS_JSON, MangaList.from_dict)
        if manga_list.add_manga(manga_id):
            print(f'Added: {manga_id}')
            FileHelper.save_json_file(Constants.general.MANGA_IDS_JSON, manga_list.to_dict())
        else:
            print(f'ID "{manga_id}" already exists.')
    try:
        manga_info = MangaHelper.get_manga_info(manga_id)
        MangaHelper.save_manga(manga=manga_info)
        # Retrieve all pattern of chapters
        chapter_patterns = FileHelper.load_json_file(Constants.general.CHAPTER_PATTERNS_JSON, ChapterPatterns.from_dict, allow_missing=True)
        for chapter in manga_info.chapters:
            chapter_patterns.add_pattern(chapter.link.split("/")[-1])
        # Saving chapter patterns
        FileHelper.save_json_file(Constants.general.CHAPTER_PATTERNS_JSON, chapter_patterns.to_dict())
        # MangaHelper.download_manga(manga=manga_info)
    except Exception as e:
        print(e)
        
def download_all_manga() -> None:
    manga_list = get_manga_ids()
    FileHelper.save_json_file(Constants.general.MANGA_IDS_JSON, manga_list.to_dict())
    for manga in manga_list.ids:
        download_manga(manga, False)
        
def check_manga(manga_id: str) -> None:
    print(f"# Checking {manga_id} ...")
    try:
        manga_info = MangaHelper.load_manga_from_json(PathHelper.get_manga_json_path(manga_id))
        for chapter in manga_info.chapters[::-1]:
            path = PathHelper.get_chapter_path(manga_id, chapter.number)
            json_path = PathHelper.get_chapter_json_path(manga_id, chapter.number)
            try:
                chapter_pages_info = ChapterHelper.load_chapter_from_json(json_path)
                # List all files that are not JSON files
                files = [
                    f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f)) and not f.endswith(".json")
                ]
                if (len(files) != len(chapter_pages_info.page_links)):
                    raise ValueError(f"missing pages")
            except ValueError as ve:
                print(f"/!\\ {manga_id} ({chapter.number}) : {ve}")
                if "Failed to load json file" in str(ve) and os.path.exists(path):
                    shutil.rmtree(path)
            except Exception as e:
                print(f"/!\\ {manga_id} ({chapter.number}) : Unable to load json file {json_path} {e}")
    except Exception as e:
        print(e)
        
def check_all_manga() -> None:
    for manga in os.listdir(Constants.general.DL_PATH):
        if os.path.isdir(os.path.join(Constants.general.DL_PATH, manga)):
            check_manga(manga)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="dl_manager.py")
    parser.add_argument('--dl', nargs=1,
                    help='download manga (use manga id as parameter)',
                    action='store', type=str)
    parser.add_argument('--dlall',
                    help='download all already known manga',
                    action="store_true")
    parser.add_argument('-c', '--check', nargs=1,
                    help='check manga files (use manga id as parameter)',
                    action='store', type=str)
    parser.add_argument('--checkall',
                    help='chack all manga integrity',
                    action="store_true")

    args = parser.parse_args(sys.argv[1:])
    
    if args.dl is not None:
        download_manga(args.dl[0], True)
        sys.exit()
    elif args.dlall:
        download_all_manga()
        sys.exit()
    elif args.check is not None:
        check_manga(args.check[0])
        sys.exit()
    elif args.checkall:
        check_all_manga()
        sys.exit()

    