import argparse
import os
import sys
from constants import Constants
from helpers.chapter_helper import ChapterHelper
from helpers.file_helper import FileHelper
from helpers.manga_helper import MangaHelper
from helpers.path_helper import PathHelper

def download_manga(manga_id: str) -> None:
    print(f"# Downloading {manga_id} ...")
    try:
        manga_info = MangaHelper.get_manga_info(manga_id)
        MangaHelper.save_manga(manga=manga_info)
        MangaHelper.download_manga(manga=manga_info)
    except Exception as e:
        print(e)
        
def download_all_manga() -> None:
    for manga in os.listdir(Constants.general.DL_PATH):
        if os.path.isdir(os.path.join(Constants.general.DL_PATH, manga)):
            download_manga(manga)
        
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
            except Exception as e:
                print(f"/!\\ {manga_id} ({chapter.number}) : Unable to load json file {json_path} {e}")
    except Exception as e:
        print(e)
        
def check_all_manga() -> None:
    for manga in os.listdir(Constants.general.DL_PATH):
        if os.path.isdir(os.path.join(Constants.general.DL_PATH, manga)):
            check_manga(manga)

if __name__ == "__main__":
    # Definition of argument option
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
    
    
    # Parsing of command line argument
    args = parser.parse_args(sys.argv[1:])
    
    if args.dl is not None:
        download_manga(args.dl[0])
        sys.exit()
    elif args.dlall is not None:
        download_all_manga()
        sys.exit()
    elif args.check is not None:
        check_manga(args.check[0])
        sys.exit()
    elif args.checkall is not None:
        check_all_manga()
        sys.exit()

    