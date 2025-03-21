import argparse
import sys

from helpers.firebase_helper import FirebaseHelper

if __name__ == "__main__":
    # Definition of argument option
    parser = argparse.ArgumentParser(prog="ul_manager.py")
    parser.add_argument('-u', '--upload', nargs=1,
                        help='upload downloaded manga to firestore (use "manga-id")',
                        action='store', type=str)
    parser.add_argument('--delete', nargs=1,
                    help='delete manga from firestore (use "manga-id")',
                    action='store', type=str)

    # Parsing of command line argument
    args = parser.parse_args(sys.argv[1:])
    
    # Initializing firebase
    firebaseHelper = FirebaseHelper()

    if args.upload is not None:
        firebaseHelper.upload_manga(args.upload[0])
        sys.exit()
    elif args.delete is not None:
        firebaseHelper.delete_manga(args.delete[0])
        sys.exit()

    