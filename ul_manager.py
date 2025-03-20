import argparse
import sys

from helpers.firebase_helper import FirebaseHelper

if __name__ == "__main__":
    # Definition of argument option
    parser = argparse.ArgumentParser(prog="ul_manager.py")
    parser.add_argument('--upload', nargs=1,
                        help='upload downloaded manga to firebase storage (use "manga-id")',
                        action='store', type=str)

    # Parsing of command line argument
    args = parser.parse_args(sys.argv[1:])
    
    # Initializing firebase
    firebaseHelper = FirebaseHelper()

    if args.upload is not None:
        firebaseHelper.upload_manga(args.upload[0])
        sys.exit()

    