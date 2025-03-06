import argparse
import sys
from constants import Constants
from helpers.file_helper import FileHelper
from helpers.manga_helper import MangaHelper

def download_manga(manga_id):
    print(f"# Downloading {manga_id} ...")
    try:
        manga_info = MangaHelper.get_manga_info(manga_id)
        MangaHelper.save_manga(manga=manga_info)
        MangaHelper.download_manga(manga=manga_info)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Definition of argument option
    parser = argparse.ArgumentParser(prog="dl_manager.py")
    parser.add_argument('--dlmanga', nargs=1,
                    help='download manga (use manga id as parameter)',
                    action='store', type=str)
    
    # Parsing of command line argument
    args = parser.parse_args(sys.argv[1:])
    
    if args.dlmanga is not None:
        download_manga(args.dlmanga[0])
        sys.exit()

    