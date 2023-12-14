from fastapi import FastAPI
from googleapiclient.discovery import build
from pprint import pprint
import requests
from google.cloud import translate

app = FastAPI()
TARGET_LANGUAGE = "zh"  # Chinese
API_KEY = "AIzaSyB9lomWP02z3mjqFrnwXz1F3hrj7J8SJGE"
OMDB_API_KEY = "your_omdb_api_key"  # Replace with your OMDB API key
PROJECT_ID = "your_project_id"  # Replace with your Google Cloud project ID

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/video")
def get_video(url: str):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    video_id = url.split("v=")[1]
    video_response = youtube.videos().list(
        part="snippet, statistics",
        id=video_id
    ).execute()

    title = video_response['items'][0]['snippet']['title']
    description = video_response['items'][0]['snippet']['description']
    category_id = video_response['items'][0]['snippet']['categoryId']
    view_count = video_response['items'][0]['statistics']['viewCount']

    category_response = youtube.videoCategories().list(
        part="snippet",
        id=category_id,
    ).execute()

    category = category_response['items'][0]['snippet']['title']

    return {
        "url": url,
        "title": title,
        "description": description,
        "view_count": view_count,
        "category": category,
    }

@app.get("/moviereviews_reviews/")
def get_youtube_reviews(url: str):
    # Extract video ID from the URL
    video_id = get_video_id_from_url(url)
    
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Get video details using the video ID
    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    # Extract video information
    video_info = video_response.get("items", [])
    if not video_info:
        raise HTTPException(status_code=404, detail="Video not found")

    title = video_info[0]["snippet"]["title"]
    description = video_info[0]["snippet"]["description"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return {
        "title": title,
        "description": description,
        "video_url": video_url
    }

@app.get("/retrieve_description")
def retrieve_full_description(url: str):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    video_id = url.split("v=")[1]
    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    description = video_response['items'][0]['snippet']['description']

    return {"url": url, "full_description": description}

@app.get("/review_in_chinese")
def review_in_chinese(url: str):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    video_id = url.split("v=")[1]
    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    description = video_response['items'][0]['snippet']['description']

    # Translate the description to Chinese using Google Cloud Translation API
    translated_description = translate_text(description, TARGET_LANGUAGE)

    return {"url": url, "original_description": description, "translated_description": translated_description}

def translate_text(text, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
