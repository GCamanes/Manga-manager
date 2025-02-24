import requests
from bs4 import BeautifulSoup
import sys

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

    chapter_links = []
    for link in soup.select(".panel-story-chapter-list a"):
        chapter_url = link.get("href")
        if chapter_url:
            chapter_links.append(chapter_url)

    return chapter_links

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <manga-id>")
        sys.exit(1)

    manga_id = sys.argv[1]  # Get the manga ID from the command-line argument
    chapter_links = get_chapter_links(manga_id)

    for chapter in chapter_links:
        print(chapter)