import requests
from bs4 import BeautifulSoup
import sys
from file_helper import download_file, convert_webp_to_png

BASE_URL = "https://chapmanganelo.com/"

def get_chapter_links(manga_id):
    manga_url = f"{BASE_URL}{manga_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(manga_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Failed to retrieve page, status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract Manga Information
    manga_info = {}
    manga_info["name"] = soup.select_one("div.story-info-right h1").text.strip() if soup.select_one("div.story-info-right h1") else "N/A"
    manga_info["picture"] = soup.select_one("div.story-info-left img")["src"] if soup.select_one("div.story-info-left img") else "N/A"

    # Extract Status
    status_tag = soup.select_one("td:-soup-contains('Status')")
    manga_info["status"] = status_tag.find_next_sibling("td").text.strip() if status_tag else "N/A"

    # Extract Last Update
    last_update_tag = soup.select_one("span.stre-label:-soup-contains('Updated :')")
    manga_info["last_update"] = last_update_tag.find_next_sibling("span").text.strip() if last_update_tag else "N/A"

    # Extract Authors
    author_tag = soup.select_one("td:-soup-contains('Author(s)')")
    manga_info["authors"] = author_tag.find_next_sibling("td").text.strip() if author_tag else "N/A"
        
    # Extract Genres (Fixed Warning)
    genre_tags = soup.select_one("td:-soup-contains('Genres')")
    manga_info["genres"] = [g.text.strip() for g in genre_tags.find_next_sibling("td").select("a")] if genre_tags else []

    chapter_links = []
    for link in soup.select(".panel-story-chapter-list a"):
        chapter_url = link.get("href")
        if chapter_url:
            chapter_links.append(chapter_url)
            
    pictureName = download_file(manga_info["picture"], "./")
    convert_webp_to_png(pictureName)

    return chapter_links, manga_info

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <manga-id>")
        sys.exit(1)

    manga_id = sys.argv[1]  # Get the manga ID from the command-line argument
    chapter_links, manga_info = get_chapter_links(manga_id)

    print(manga_info)
    
    