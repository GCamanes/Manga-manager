import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from constants import Constants
from entities.chapter_customs import ChapterCustomsEntry
from entities.chapter_pages_info import ChapterPagesInfo
from helpers.file_helper import FileHelper
from helpers.path_helper import PathHelper

class ChapterHelper:
    
    @staticmethod
    def extract_chap_number_from_link(link: str, customs: ChapterCustomsEntry = None) -> str:
        # Removing useless parts of the link
        chapter_part = link.split("/")[-1]        
        # Applyng custom or removing chapter id
        chapter_part = (customs.get_entry(chapter_part) if customs else None) or re.sub(r'^\d+', '', chapter_part)
        match = re.fullmatch(Constants.chapter.CLASSIC_REGEXP, chapter_part)
        match_customs = re.fullmatch(Constants.chapter.CUSTOM_REGEXP, chapter_part)
        if match:
            first_digits = match.group(2)
            last_digits = match.group(3) if match.group(3) else None
            return f"{first_digits.zfill(4)}.{last_digits.zfill(2)}" if last_digits is not None else first_digits.zfill(4)
        elif match_customs:
            first_digits = match_customs.group(1)
            last_digits = match_customs.group(2) if match_customs.group(2) else None
            return f"{first_digits.zfill(4)}.{last_digits.zfill(2)}" if last_digits is not None else first_digits.zfill(4)
        
        return chapter_part
    
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
        FileHelper.save_json_file(path, chapter_pages_info.to_dict())

    @staticmethod
    def load_chapter_from_json(filepath: str) -> ChapterPagesInfo:
        return FileHelper.load_json_file(filepath, ChapterPagesInfo.from_dict)