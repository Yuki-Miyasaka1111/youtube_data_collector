from fastapi import FastAPI
from youtube import get_video_info

app = FastAPI()

@app.get("/video/{video_id}")
def read_video_info(video_id: str):
    return get_video_info(video_id)
