import json
import firebase_admin
from firebase_admin import credentials, firestore, storage

from constants import Constants
from helpers.manga_helper import MangaHelper

class FirebaseHelper:
    def __init__(self):
        # Cloud Firestore certificate
        self.cred = credentials.Certificate(Constants.firebase.service_account_key)
        self.app = firebase_admin.initialize_app(self.cred, {'storageBucket': self.__getStorageUrl()})
        # Get firestore client to interact with distant database
        self.store = firestore.client()
    
    def __getStorageUrl(self):
        storageUrl = None
        try:
            with open(Constants.firebase.service_account_key, "r") as fp:
                jsonObject = json.load(fp)
                storageUrl = '{}.appspot.com'.format(jsonObject['project_id'])
        except:
            pass
        return storageUrl
    
    def upload_manga(self, manga_id):
        print(f"# Uploading {manga_id} ...")
        manga = MangaHelper.load_manga_from_json(MangaHelper.get_manga_json_path(manga_id))
        manga_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga.id)
        manga_ref.set(manga.to_dict_without_link())