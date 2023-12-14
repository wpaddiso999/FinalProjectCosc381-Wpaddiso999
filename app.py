from fastapi import FastAPI
from googleapiclient.discovery import build
from pprint import pprint

app = FastAPI()

API_KEY = "AIzaSyB9lomWP02z3mjqFrnwXz1F3hrj7J8SJGE"

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
    print("title -", title)
    print("Description -", description)
    print("Category ID - ", category_id)
    print("View Count -", view_count)

    category_response = youtube.videoCategories().list(
        part="snippet",
        id=category_id,
    ).execute()

    pprint(category_response)
    category = category_response['items'][0]['snippet']['title']
    print(category)

    return {
        "url": url,
        "title": title,
        "description": description,
        "view_count": view_count,
        "category": category,
    }

@app.get("/search_reviews")
def search_movie_reviews(url: str):
    # Implement the method to search for movie reviews based on the YouTube URL
    # You can use external libraries or APIs to perform this task

    # Placeholder response for now
    return {"message": "Searching for movie reviews..."}

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
    # Implement the method to review the video and provide description in Chinese
    # You can use translation APIs to perform this task

    # Placeholder response for now
    return {"message": "Reviewing in Chinese..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
