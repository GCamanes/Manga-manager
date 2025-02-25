import sys
from helpers.manga_helper import MangaHelper

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <manga-id>")
        sys.exit(1)

    manga_id = sys.argv[1]  # Get the manga ID from the command-line argument
    manga_info = MangaHelper.get_manga_info(manga_id)
    print(manga_info)

    