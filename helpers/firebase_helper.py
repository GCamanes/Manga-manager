import json
from uuid import uuid4
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
    
    def __upload_file(self, local_path, storage_path):
        # Create blob
        bucket = storage.bucket()
        blob = bucket.blob(storage_path)
        # Create new token
        new_token = uuid4()
        # Create new dictionary with the metadata
        metadata = {"firebaseStorageDownloadTokens": new_token}
        # Set metadata to blob and upload
        blob.metadata = metadata
        blob.upload_from_filename(local_path)
    
    def upload_manga(self, manga_id):
        print(f"# Uploading {manga_id} ...")
        manga = MangaHelper.load_manga_from_json(MangaHelper.get_manga_json_path(manga_id))
        manga_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga.id)
        manga_ref.set(manga.to_dict_without_link())
        self.__upload_file(f"{Constants.general.DL_PATH}/{manga.cover_path}", manga.cover_path)