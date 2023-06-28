import os
from googleapiclient.discovery import build

api_key = os.environ.get('AIzaSyAbODGQmdWfNidUwoxU1FgZnW2aC93FeGc')

youtube = build("youtube", "v3", developerKey=api_key)

def get_video_info(video_id):
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    return response
