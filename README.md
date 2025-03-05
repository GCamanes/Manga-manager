# Manga-manager
Python package to handle manga download and upload to firebase


## Run python env and pip install requirements

python3 -m venv myenv       => creation
source myenv/bin/activate   => activation
deactivate                  => quit

pip3 install requests beautifulsoup4 pillow selenium firebase-admin
brew install chromedriver

## Firebase config

Download the service account key under ServiceAccountKey.json file and place it at the project root.

## Run script 

python3 dl_manager.py --dlmanga mangaID

