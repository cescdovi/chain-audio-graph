import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DATA_DIR = os.getenv("DATA_DIR")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")

def get_urls_from_playlist(playlist_id = PLAYLIST_ID):
    """
    Retrieve video IDs from a specified YouTube playlist and save their metadata locally.

    This function uses the YouTube Data API v3 to:
      1. Fetch all video IDs from the given playlist (handles pagination for playlists with more than 50 items).
      2. For each video ID, request its title and description.
      3. Store each video's metadata as a JSON file in a dedicated folder within DATA_DIR.

    Parameters
    ----------
    playlist_id : str, optional
        The ID of the YouTube playlist to process. Defaults to the PLAYLIST_ID
        environment variable loaded from the .env file.

    Returns
    -------
    list of str
        A list containing the video IDs found in the playlist, in the order returned by the API.
    """
    
    youtube = build(
        serviceName = 'youtube', 
        version = 'v3', 
        developerKey = YOUTUBE_API_KEY
        )
    
    videos = []
    next_page_token = None

    try:
        while True:
            request = youtube.playlistItems().list(
                part       = "contentDetails",
                playlistId = playlist_id,
                maxResults = 50,           
                pageToken  = next_page_token
            )
            response = request.execute()

            for item in response.get('items', []):
                vid = item['contentDetails']['videoId']
                videos.append(vid)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

    except HttpError as e:
        print(f"Se produjo un error en la API: {e}")
 
    try:
        for video in videos:
            videos_dict = {}
            request = youtube.videos().list(
                part="snippet",
                id=video
                )
            response = request.execute()
            items = response.get("items", [])
            
            _video_id = items[0]["id"]
            title = items[0]["snippet"]["title"]
            description = items[0]["snippet"]["description"]

            videos_dict[_video_id] = {
                "title": title,
                "description": description
            }

            output_dir = Path(DATA_DIR) / _video_id
            output_dir.mkdir(parents=True, exist_ok=True)
            metadata_path = output_dir / "metadata.json"

            with open((metadata_path), "w", encoding="utf-8") as f:
                json.dump(videos_dict, f, ensure_ascii=False, indent=2)

    except HttpError as e:
        print(f"Se produjo un error en la API: {e}")

    return videos