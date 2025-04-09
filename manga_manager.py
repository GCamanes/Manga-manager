import argparse
import sys

from managers.download_manager import DownloadManager

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
        DownloadManager.download_manga(args.dl[0], True)
        sys.exit()
    elif args.dlall:
        DownloadManager.download_all_manga()
        sys.exit()
    elif args.check is not None:
        DownloadManager.check_manga(args.check[0])
        sys.exit()
    elif args.checkall:
        DownloadManager.check_all_manga()
        sys.exit()