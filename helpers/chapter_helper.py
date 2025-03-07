import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from constants import Constants
from entities.chapter_pages_info import ChapterPagesInfo
from entities.manga_info import MangaInfo
from helpers.path_helper import PathHelper

class ChapterHelper:
    @staticmethod
    def get_matching_link(link: str) -> str:
        for filter_text in Constants.chapter.FILTERS:
            if filter_text in link:
                return filter_text
        return None
    
    @staticmethod
    def extract_chap_number_from_link(link: str) -> str:
        filter_text = ChapterHelper.get_matching_link(link)
        chapter_parts = link.split(filter_text)[-1].split("-")
        chapter_parts[0] = str(chapter_parts[0]).zfill(4)
        return ".".join(chapter_parts[:2])
    
    @staticmethod
    def get_chapter_pages_list(link: str) -> list[str]:
        try:
            chapter_url = f"{Constants.general.WEBSITE}{link}"
            
            # Set up Selenium WebDriver
            service = Service("/opt/homebrew/bin/chromedriver")  # Change this to your ChromeDriver path
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run without opening a browser
            driver = webdriver.Chrome(service=service, options=options)
            
            # Load the webpage
            driver.get(chapter_url)
            
            # Wait for at least one <div data-name="image-item"> to appear
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@data-name="image-item"]'))
                )
            except Exception as e:
                raise ValueError(f"Error waiting for elements for {link}. {e}")

            # Get the fully loaded page source
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            # Close the browser
            driver.quit()
            
            # Get image links
            image_links = []
            main_element = soup.select_one('main')
            image_divs = main_element.find_all("div", {"data-name": "image-item"})
            for image_div in image_divs:
                image_link = image_div.select_one('img').get("src")
                image_links.append(image_link)
            
            return image_links
        except Exception as e:
            raise e
        
    @staticmethod
    def save_chapter_to_json(chapter_pages_info: ChapterPagesInfo) -> None:
        path = PathHelper.get_chapter_json_path(chapter_pages_info.manga_id, chapter_pages_info.number)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(chapter_pages_info.to_dict(), f, indent=4)
        except Exception as e:
            raise ValueError(f"Failed to save json file {path} {e}")

    @staticmethod
    def load_chapter_from_json(filename: str) -> ChapterPagesInfo:
        try:
            if not os.path.exists(filename):
                raise ValueError(f"Failed to load json file {filename}")
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return ChapterPagesInfo.from_dict(data)
        except Exception as e:
            raise e