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

# class Comment(BaseModel):
#     text: str
#     author: str
#     date: str

class Thumbnail(BaseModel):
    url: str

class Thumbnails(BaseModel):
    default: Optional[Thumbnail]

class Video(BaseModel):
    title: str
    description: str
    publishedAt: str
    thumbnails: Thumbnails
    category: Optional[str]
    tags: Optional[List[str]]
    viewCount: Optional[int]
    likeCount: Optional[int]
    # dislikeCount: Optional[int]
    commentCount: Optional[int]
    favoriteCount: Optional[int]
    channelTitle: Optional[str]
    channelDescription: Optional[str]
    subscriberCount: Optional[int]
    totalViews: Optional[int]
    totalVideos: Optional[int]
    # playlistTitle: Optional[str]
    # playlistDescription: Optional[str]
    # playlistVideoCount: Optional[int]
    # comments: Optional[List[Comment]]

@app.get("/videos")
async def get_videos(channelId: str, apiKey: str):
    controller = YoutubeController(api_key=apiKey)
    videos = controller.get_all_videos(youtubech_id=channelId)
    # 必要な情報だけを抽出して返却
    return [
        Video(
            title=video['title'],
            description=video['description'],
            publishedAt=video['publishedAt'],
            thumbnails=Thumbnails(default=Thumbnail(url=video['thumbnails']['default']['url'])),
            category=video.get('category'),
            tags=video.get('tags'),
            viewCount=int(video['viewCount']),
            likeCount=int(video['likeCount']),
            commentCount=int(video['commentCount']),
            favoriteCount=int(video['favoriteCount']),
            channelTitle=video['channelTitle'],
            channelDescription=video.get('channelDescription'),
            subscriberCount=int(video.get('subscriberCount', 0)),
            totalViews=int(video.get('totalViews', 0)),
            totalVideos=int(video.get('totalVideos', 0)),
            # playlistTitle=video.get('playlistTitle'),
            # playlistDescription=video.get('playlistDescription'),
            # playlistVideoCount=int(video.get('playlistVideoCount', 0)),
            # comments=[Comment(text=c['text'], author=c['author'], date=c['date']) for c in video.get('comments', [])]
        ) for video in videos
    ]