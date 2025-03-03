import json
import os
import re
from bs4 import BeautifulSoup
import requests
from constants import Constants
from entities.chapter_info import ChapterInfo
from entities.manga_info import MangaInfo
from helpers.chapter_helper import ChapterHelper
from helpers.file_helper import FileHelper

class MangaHelper:
    @staticmethod
    def get_manga_info(manga_id):
        manga_url = f"{Constants.general.BASE_URL}{manga_id}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        response = requests.get(manga_url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Failed to retrieve page, status code {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        
        # get main div
        main_element = soup.select_one('main')
        
        # Extract manga title
        title = main_element.select_one('a.link.link-hover').text.strip()
        # Extract genres
        genres_tag = main_element.select_one('b', string='Genres:')
        genres_parent = genres_tag.find_parent('div')
        genres = [child.get('q:key') for child in genres_parent.children if child.name == 'span']
        # Extract authors
        authors = []
        for a_tag in main_element.select_one('div').select_one('div').find_all('a'):
            href = a_tag.get('href')
            if href and "/search" in href:
                authors.append(a_tag.get_text().strip())
        # Extract status
        status_tag = main_element.select_one('span:-soup-contains("Original Publication:")')
        status_parent = status_tag.find_parent('div')
        status = status_parent.select_one('span.font-bold.uppercase').text.strip()
        # Extract image URL
        cover_path = main_element.select_one('img').get("src")

        # Extract chapters list
        chapter_list_div = soup.find('div', attrs={'data-name': 'chapter-list'})
        ## Find all <a> tags that match the manga pattern
        matching_links = chapter_list_div.find_all('a', href=re.compile(rf"^/title/{re.escape(manga_id)}/.*"))
        ## Filter links containing "ch." or "chapter-" in lower case
        filtered_links = [
            link for link in matching_links
            if ChapterHelper.get_matching_link(link.get("href")) != None
        ]
        chapters = [ChapterInfo(ChapterHelper.extract_chap_number_from_link(link.get("href")), link.get("href")) for link in filtered_links]
            
        #pictureName = download_file(image_url, "./")
        #convert_webp_to_png(pictureName)
        
        return MangaInfo(manga_id, title, cover_path, authors, genres, status, chapters)
    
    @staticmethod
    def get_manga_path(id: str):
        return f"{Constants.general.DL_PATH}/{id}/"
    
    @staticmethod
    def download_cover(manga: MangaInfo):
        return manga
    
    @staticmethod
    def get_manga_json_path(id: str):
        return f"{MangaHelper.get_manga_path(id)}{id}.json"

    @staticmethod
    def save_manga_to_json(manga: MangaInfo):
        with open(MangaHelper.get_manga_json_path(manga.id), "w", encoding="utf-8") as f:
            json.dump(manga.to_dict(), f, indent=4)

    @staticmethod
    def load_manga_from_json(filename: str) -> MangaInfo | None:
        if not os.path.exists(filename):
            return None
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return MangaInfo.from_dict(data)
    
    @staticmethod
    def save_manga(manga: MangaInfo):
        FileHelper.create_folder(f"{Constants.general.DL_PATH}/{manga.id}")
        cover_path = FileHelper.download_file(manga.cover_path, MangaHelper.get_manga_path(manga.id), manga.id)
        cover_path = FileHelper.convert_webp_to_png(cover_path)
        manga.cover_path = "/".join(cover_path.split("/")[1:])
        MangaHelper.save_manga_to_json(manga)