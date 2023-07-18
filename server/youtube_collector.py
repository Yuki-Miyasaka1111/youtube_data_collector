import os
import requests
import json
from fastapi import HTTPException

class YoutubeController:
    def __init__(self, api_key):
        self.youtube_apikey = api_key
        self.ch_info = None
        self.upload_list_id = None
        self.all_videos = []

    def get_all_videos(self, youtubech_id=None):
        play_list_id = self._get_playlist(play_list_name = "uploads", youtubech_id=youtubech_id)
        print(play_list_id)
        play_list_videos = self._get_playlist_videos(play_list_id=play_list_id)
        videos_statistics = self._get_statistics_data(play_list_videos=play_list_videos)
        self.all_videos = self._combine_snippet_statistics_data(play_list_videos=play_list_videos, videos_statistics=videos_statistics)

        return self.all_videos
    
    def _get_playlist(self, youtubech_id, play_list_name = "uploads",):
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = dict(
            key=self.youtube_apikey,
            part="contentDetails",
            id=youtubech_id
        )
        res = requests.get(url=url, params=params)

        if res.status_code == 400:
            obj = res.json()
            raise HTTPException(
                status_code=obj['error']['code'],
                detail = "エラー：APIキーを確認してください。"
            )
        
        res_json = res.json()
        play_list_id = res_json['items'][0]['contentDetails']['relatedPlaylists'][play_list_name]
        return play_list_id
    
    def _get_playlist_videos(self, play_list_id):
        """play_list_idに登録されている動画リストを取得

        :param play_list_id
        :return
        """
        play_list_videos = []
        page_token = None
        url = "https://www.googleapis.com/youtube/v3/playlistItems"
        while True:
            params = dict(
                key=self.youtube_apikey,
                part="snippet",
                playlistId=play_list_id,
                maxResults=50,
                pageToken=page_token
            )
            res = requests.get(url=url, params=params)
            print(res)

            # Check if the request was successful
            if res.status_code != 200:
                print(f"Request failed with status code {res.status_code}")
                return None

            try:
                res_json = res.json()
            except json.decoder.JSONDecodeError:
                print("Failed to decode the response")
                return None

            # Check if 'items' key exists in the response
            if 'items' not in res_json:
                print("'items' key not found in the response")
                return None

            play_list_videos.extend(res_json['items'])

            try:
                page_token = res_json['nextPageToken']
            except KeyError as e:
                break

        return play_list_videos

    def _get_statistics_data(self, play_list_videos):
        videos_statistics = []
        url = "https://www.googleapis.com/youtube/v3/videos"

        # 取得する動画のidリストの作成
        videos_id_list = [video['snippet']['resourceId']['videoId'] for video in play_list_videos]

        # idリストをsplit_numで分割
        split_num = 50 # 分割したい個数
        split_videos_id_list = [videos_id_list[n:n+split_num] for n in range(0, len(videos_id_list), split_num)]

        # 分割したid_listごとにデータを取得する
        for split_videos_ids in split_videos_id_list:
            params = dict(
                key=self.youtube_apikey,
                part="statistics",
                id=','.join(split_videos_ids),
                maxResults=50,
            )
            res = requests.get(url=url, params=params)
            res_json = res.json()
            videos_statistics.extend(res_json['items'])

        return videos_statistics
    
    def _get_comments(self, video_id):
        """Get comments of a video

        :param video_id
        :return
        """
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = dict(
            key=self.youtube_apikey,
            part="snippet",
            videoId=video_id,
            maxResults=20,  # Change this value to get more comments
        )
        res = requests.get(url=url, params=params)
        res_json = res.json()
        comments = [{"text": item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    "author": item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    "date": item['snippet']['topLevelComment']['snippet']['publishedAt']}
                    for item in res_json['items']]

        return comments
    
    def _get_channel_info(self, channel_id):
        """Get information of a channel

        :param channel_id
        :return
        """
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = dict(
            key=self.youtube_apikey,
            part="snippet,statistics",
            id=channel_id,
        )
        res = requests.get(url=url, params=params)
        res_json = res.json()
        channel_info = {
            "title": res_json['items'][0]['snippet']['title'],
            "description": res_json['items'][0]['snippet']['description'],
            "subscriberCount": res_json['items'][0]['statistics']['subscriberCount'],
            "totalViews": res_json['items'][0]['statistics']['viewCount'],
            "totalVideos": res_json['items'][0]['statistics']['videoCount'],
        }

        return channel_info
    
    def _get_playlist_info(self, playlist_id):
        """Get information of a playlist

        :param playlist_id
        :return
        """
        url = "https://www.googleapis.com/youtube/v3/playlists"
        params = dict(
            key=self.youtube_apikey,
            part="snippet,contentDetails",
            id=playlist_id,
        )
        res = requests.get(url=url, params=params)
        res_json = res.json()
        playlist_info = {
            "title": res_json['items'][0]['snippet']['title'],
            "description": res_json['items'][0]['snippet']['description'],
            "videoCount": res_json['items'][0]['contentDetails']['itemCount'],
        }

        return playlist_info
    
    def _combine_snippet_statistics_data(self, play_list_videos, videos_statistics):
        all_videos = []
        for video in play_list_videos:
            for videos_statistic in videos_statistics:
                if video['snippet']['resourceId']['videoId'] == videos_statistic['id']:
                    print('Video Snippet:', video['snippet'])  # Add this line
                    print('Video Statistics:', videos_statistic['statistics'])  # Add this line
                    combined_data = {**video['snippet'], **videos_statistic['statistics']}
                    print('Combined Data:', combined_data)  # Add this line
                    all_videos.append(combined_data)

        return all_videos
    


if __name__ == "__main__":
    y_ctrl = YoutubeController(api_key=os.environ['api_key'])
    y_ctrl.get_all_videos(youtubech_id=os.environ['ch_id'])