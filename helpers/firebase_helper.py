import json
import math
import os
import sys
from uuid import uuid4
import firebase_admin
from firebase_admin import credentials, firestore, storage

from constants import Constants
from entities.chapter_doc import ChapterDoc
from entities.manga_doc import MangaDoc
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
    
    # Function to get a manga by ID
    def get_manga_by_id(self, manga_id):
        doc_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga_id)  # Reference to the document
        doc = doc_ref.get()  # Fetch the document
        
        if doc.exists:
            return MangaDoc.from_dict(doc.to_dict())
        else:
            return None
        
        # Function to delete a manga by ID
    def delete_manga(self, manga_id):
        manga_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga_id)
        chapters_col = manga_ref.collection(Constants.firebase.chapters_collection)
        self.__delete_collection(chapters_col, 50)
        manga_ref.delete()
        
    def __delete_collection(self, coll_ref, batch_size):
        if batch_size == 0:
            return
        docs = coll_ref.list_documents(page_size=batch_size)
        deleted = 0
        for doc in docs:
            doc.delete()
            deleted = deleted + 1
        if deleted >= batch_size:
            return self.__delete_collection(coll_ref, batch_size)
    
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
        
    def __get_all_chapters(self, manga_doc: MangaDoc) -> list[ChapterDoc]:
        chapter_docs = []
        manga_path = PathHelper.get_manga_path(manga_doc.id)
        directories = sorted([d for d in os.listdir(manga_path) if os.path.isdir(os.path.join(manga_path, d))])
        for directory in directories:
            chapter_path = f"{manga_path}/{directory}"
            pages = [f"{manga_doc.id}/{directory}/{f}" for f in os.listdir(chapter_path) if os.path.isfile(os.path.join(chapter_path, f))]
            chapter_doc = ChapterDoc(directory, pages)
            chapter_docs.append(chapter_doc)
        return chapter_docs
    
    def upload_manga(self, manga_id: str) -> None:
        print(f"# Uploading {manga_id} ...")
        # Get manga doc from firestore
        manga_doc = self.get_manga_by_id(manga_id)
        # Load local manga info
        manga = MangaHelper.load_manga_from_json(PathHelper.get_manga_json_path(manga_id))

        # Create a maga docucment on firestore
        if (manga_doc == None):
            manga_doc = MangaDoc(manga.id, manga.title, manga.cover_path, manga.authors, manga.genres, manga.status)
            manga_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga_doc.id)
            manga_ref.set(manga_doc.to_dict())
            self.__upload_file(f"{Constants.general.DL_PATH}/{manga_doc.cover_path}", manga_doc.cover_path)
        # Update manga status
        else:
            manga_doc.status = manga.status

        # Get all chapters from directories
        chapter_docs = self.__get_all_chapters(manga_doc)
        # Upload each chapter and update manga doc accordingly
        for chapter_doc in chapter_docs:
            if chapter_doc.number not in manga_doc.chapters:
                try:
                    sys.stdout.write(f"\r\033[K* chapter {chapter_doc.number} ...")
                    sys.stdout.flush()
                    for index, page in enumerate(chapter_doc.pages):
                        percent = math.floor((index + 1) * 100 / len(chapter_doc.pages))
                        barIndex = math.floor(percent/10) 
                        bar = "#" * barIndex + " " * (10 - barIndex)
                        self.__upload_file(f"{Constants.general.DL_PATH}/{page}", page)
                        sys.stdout.write(f"\r\033[K* chapter {chapter_doc.number} : [{bar}] {percent}%")
                        sys.stdout.flush()
                    chapter_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga_doc.id)\
                        .collection(Constants.firebase.chapters_collection).document(chapter_doc.number)
                    chapter_ref.set(chapter_doc.to_dict())
                    manga_doc.chapters.append(chapter_doc.number)
                    manga_ref = self.store.collection(Constants.firebase.mangas_collection).document(manga_doc.id)
                    manga_ref.set(manga_doc.to_dict())
                except Exception as e:
                    print(f"/!\\ ERROR while uplaoding {manga_id} {chapter_doc.number} : {e}")
                    sys.exit(1)