import json
from uuid import uuid4
import firebase_admin
from firebase_admin import credentials, firestore, storage

from constants import Constants
from entities.manga_info_doc import MangaInfoDoc
from helpers.manga_helper import MangaHelper
from helpers.path_helper import PathHelper

class FirebaseHelper:
    def __init__(self):
        # Cloud Firestore certificate
        self.cred = credentials.Certificate(Constants.firebase.service_account_key)
        self.app = firebase_admin.initialize_app(self.cred, {'storageBucket': self.__getStorageUrl()})
        # Get firestore client to interact with distant database
        self.store = firestore.client()
    
    def __getStorageUrl(self) -> str | None:
        storageUrl = None
        try:
            with open(Constants.firebase.service_account_key, "r") as fp:
                jsonObject = json.load(fp)
                storageUrl = '{}.appspot.com'.format(jsonObject['project_id'])
        except:
            pass
        return storageUrl
    
    # Function to get a document by ID
    def get_manga_by_id(self, manga_id):
        doc_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga_id)  # Reference to the document
        doc = doc_ref.get()  # Fetch the document
        
        if doc.exists:
            return MangaInfoDoc.from_dict(doc.to_dict())
        else:
            print("No such document found!")
            return None
    
    def __upload_file(self, local_path: str, storage_path: str) -> None:
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
    
    def upload_manga(self, manga_id: str) -> None:
        print(f"# Uploading {manga_id} ...")
        manga_previous = self.get_manga_by_id(manga_id)
        print(manga_previous)
        manga = MangaHelper.load_manga_from_json(PathHelper.get_manga_json_path(manga_id))
        manga_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga.id)
        manga_ref.set(manga.to_dict_without_link())
        self.__upload_file(f"{Constants.general.DL_PATH}/{manga.cover_path}", manga.cover_path)