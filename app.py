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

def youtube_search(query, max_results=10):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id",
        maxResults=max_results
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    return video_ids

@app.get("/moviereviews_reviews/")
def get_youtube_reviews(movie_name: str):
    # Search for videos related to the movie
    video_ids = youtube_search(movie_name)
    
    if not video_ids:
        raise HTTPException(status_code=404, detail=f"No videos found for the movie: {movie_name}")

    youtube = build("youtube", "v3", developerKey=API_KEY)

    reviews = []
    for video_id in video_ids:
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        video_info = video_response.get("items", [])
        if not video_info:
            continue

        title = video_info[0]["snippet"]["title"]
        description = video_info[0]["snippet"]["description"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        reviews.append({
            "title": title,
            "description": description,
            "video_url": video_url
        })

    return {"movie_name": movie_name, "reviews": reviews}

def youtube_search(query, max_results=10):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id",
        maxResults=max_results,
        relevanceLanguage="zh"  # Set the language to Chinese
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    return video_ids

@app.get("/reviews_in_chinese/")
def reviews_in_chinese(movie_name: str):
    # Search for videos related to the movie in Chinese
    video_ids = youtube_search(movie_name)

    if not video_ids:
        raise HTTPException(status_code=404, detail=f"No videos found for the movie: {movie_name}")

    youtube = build("youtube", "v3", developerKey=API_KEY)

    reviews = []
    for video_id in video_ids:
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        video_info = video_response.get("items", [])
        if not video_info:
            continue

        title = video_info[0]["snippet"]["title"]
        description = video_info[0]["snippet"]["description"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        reviews.append({
            "title": title,
            "description": description,
            "video_url": video_url
        })

    return {"movie_name": movie_name, "reviews": reviews}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
