import argparse
import sys

from helpers.firebase_helper import FirebaseHelper
from helpers.download_helper import DownloadHelper

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
    parser.add_argument('-u', '--upload', nargs=1,
                    help='upload downloaded manga to firestore (use "manga-id")',
                    action='store', type=str)
    parser.add_argument('--delete', nargs=1,
                    help='delete manga from firestore (use "manga-id")',
                    action='store', type=str)

    args = parser.parse_args(sys.argv[1:])
    
    if args.dl is not None:
        DownloadHelper.download_manga(args.dl[0], True)
        sys.exit()
    elif args.dlall:
        DownloadHelper.download_all_manga()
        sys.exit()
    elif args.check is not None:
        DownloadHelper.check_manga(args.check[0])
        sys.exit()
    elif args.checkall:
        DownloadHelper.check_all_manga()
        sys.exit()

    # Initializing firebase
    firebaseHelper = FirebaseHelper()

    if args.upload is not None:
        firebaseHelper.upload_manga(args.upload[0])
        sys.exit()
    elif args.delete is not None:
        firebaseHelper.delete_manga(args.delete[0])
        sys.exit()

    sys.exit()