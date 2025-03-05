import argparse
import sys
from constants import Constants
import firebase_admin
from firebase_admin import credentials, firestore, storage

def upload_manga(manga_id):
    print(f"# Uploading {manga_id} ...")

if __name__ == "__main__":
    # Definition of argument option
    parser = argparse.ArgumentParser(prog="ul_manager.py")
    parser.add_argument('--upload', nargs=1,
                        help='upload downloaded manga to firebase storage (use "manga-id")',
                        action='store', type=str)

    # Parsing of command line argument
    args = parser.parse_args(sys.argv[1:])

    if args.upload is not None:
        upload_manga(args.upload[0])
        sys.exit()

    