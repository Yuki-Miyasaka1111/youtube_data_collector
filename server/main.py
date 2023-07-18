from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from youtube_collector import YoutubeController

app = FastAPI()

origins = [
    "http://localhost:3000" # Reactアプリのオリジン
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Video(BaseModel):
    title: str
    description: str
    publishedAt: str

@app.get("/videos")
async def get_videos(channelId: str, apiKey: str):
    controller = YoutubeController(api_key=apiKey)
    videos = controller.get_all_videos(youtubech_id=channelId)
    # 必要な情報だけを抽出して返却
    return [
        Video(
            title=video['title'],
            description=video['description'],
            publishedAt=video['publishedAt']
            # 他に必要なフィールドがあれば追加
        ) for video in videos
    ]