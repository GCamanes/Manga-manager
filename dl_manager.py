import requests
from bs4 import BeautifulSoup
import sys
from entities.chapter import Chapter
from entities.manga_info import MangaInfo
from file_helper import download_file, convert_webp_to_png

BASE_URL = "https://mangapark.io/title/"

def get_manga_info(manga_id):
    manga_url = f"{BASE_URL}{manga_id}"
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
    #status_elem = soup.select_one('.meta span:-soup-contains("Status")')
    #status = status_elem.find_next_sibling("span").text.strip() if status_elem else "Unknown"
    # Extract last updated
    #last_updated_elem = soup.select_one('.meta span:-soup-contains("Updated")')
    #last_updated = last_updated_elem.find_next_sibling("span").text.strip() if last_updated_elem else "Unknown"
    # Extract image URL
    #image_url = soup.select_one(".manga-thumbnail img")["src"]

    ###chapters = []
    #for chapter in soup.select(".chapter-list a"):
    #    chapter_url = chapter["href"]
    #    chapters.append(Chapter("https://mangafire.to" + chapter_url))
        
    #pictureName = download_file(image_url, "./")
    #convert_webp_to_png(pictureName)
    
    return MangaInfo(manga_id, title, authors, genres, status, None, None)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <manga-id>")
        sys.exit(1)

    manga_id = sys.argv[1]  # Get the manga ID from the command-line argument
    manga_info = get_manga_info(manga_id)
    print(manga_id)
    print(manga_info)

    