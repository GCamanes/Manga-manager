import argparse
import sys
from helpers.manga_helper import MangaHelper

if __name__ == "__main__":
    # Definition of argument option
    parser = argparse.ArgumentParser(prog="dl_manager.py")
    parser.add_argument('--dlmanga', nargs=1,
                    help='download manga (use manga id as parameter)',
                    action='store', type=str)
    
    # Parsing of command line argument
    args = parser.parse_args(sys.argv[1:])
    
    if args.dlmanga is not None:
        manga_info = MangaHelper.get_manga_info(args.dlmanga[0])
        print(manga_info)
        sys.exit()

    