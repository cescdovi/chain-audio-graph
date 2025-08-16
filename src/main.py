from src.playlist_extractor import get_urls_from_playlist
import os
from dotenv import load_dotenv

load_dotenv()

PLAYLIST_ID = os.getenv("PLAYLIST_ID")

if __name__ == "__main__":
    urls = get_urls_from_playlist(playlist_id = PLAYLIST_ID)
    print(urls)