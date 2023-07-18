import json
import requests

def get_video_data(api_key, video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key": api_key,
        "part": "snippet,statistics",
        "id": video_id,
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(json.dumps(data, indent=4))

# Replace with your API key and video ID
get_video_data("AIzaSyAbODGQmdWfNidUwoxU1FgZnW2aC93FeGc", "q-jF9zS16os")
