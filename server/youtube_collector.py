import os
import requests
import json
import csv
from typing import Optional
from fastapi import HTTPException

class YoutubeController:
    def __init__(self, api_key):
        self.youtube_apikey = api_key
        self.ch_info = None
        self.upload_list_id = None
        self.all_videos = []

    def _handle_request_errors(self, res):
        if res.status_code != 200:
            print(f"Request failed with status code {res.status_code}")
            raise HTTPException(status_code=res.status_code, detail=res.text)
        return res.json()

    def get_all_videos(self, youtubech_id=None):
        play_list_id = self._get_playlist(youtubech_id=youtubech_id)
        play_list_videos = self._get_playlist_videos(play_list_id=play_list_id)
        videos_statistics = self._get_statistics_data(play_list_videos=play_list_videos)
        channel_info = self._get_channel_info(youtubech_id)
        self.all_videos = self._combine_snippet_statistics_data(play_list_videos, videos_statistics, channel_info)
        return self.all_videos

    def _get_playlist(self, youtubech_id):
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = dict(
            key=self.youtube_apikey,
            part="contentDetails",
            id=youtubech_id
        )
        res = requests.get(url=url, params=params)
        res_json = self._handle_request_errors(res)
        return res_json['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    def _get_playlist_videos(self, play_list_id, max_results=50):
        play_list_videos = []
        page_token = None
        url = "https://www.googleapis.com/youtube/v3/playlistItems"
        while True:
            params = dict(
                key=self.youtube_apikey,
                part="snippet",
                playlistId=play_list_id,
                maxResults=max_results,
                pageToken=page_token
            )
            res = requests.get(url=url, params=params)
            res_json = self._handle_request_errors(res)

            play_list_videos.extend(res_json['items'])
            page_token = res_json.get('nextPageToken')
            if not page_token:
                break

        return play_list_videos

    def _get_statistics_data(self, play_list_videos):
        videos_statistics = []
        url = "https://www.googleapis.com/youtube/v3/videos"
        videos_id_list = [video['snippet']['resourceId']['videoId'] for video in play_list_videos]
        split_num = 50
        split_videos_id_list = [videos_id_list[n:n+split_num] for n in range(0, len(videos_id_list), split_num)]

        for split_videos_ids in split_videos_id_list:
            params = dict(
                key=self.youtube_apikey,
                part="statistics",
                id=','.join(split_videos_ids),
                maxResults=50
            )
            res = requests.get(url=url, params=params)
            res_json = self._handle_request_errors(res)
            videos_statistics.extend(res_json['items'])

        return videos_statistics

    def _get_channel_info(self, channel_id):
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = dict(
            key=self.youtube_apikey,
            part="snippet,statistics",
            id=channel_id
        )
        res = requests.get(url=url, params=params)
        res_json = self._handle_request_errors(res)
        channel_info = {
            "channelTitle": res_json['items'][0]['snippet']['title'],
            "channelDescription": res_json['items'][0]['snippet']['description'],
            "subscriberCount": res_json['items'][0]['statistics']['subscriberCount'],
            "totalViews": res_json['items'][0]['statistics']['viewCount'],
            "totalVideos": res_json['items'][0]['statistics']['videoCount']
        }
        return channel_info

    def _get_video_details(self, video_id):
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = dict(
            key=self.youtube_apikey,
            part="snippet",
            id=video_id
        )
        res = requests.get(url=url, params=params)
        res_json = self._handle_request_errors(res)
        return res_json['items'][0]['snippet']

    def _combine_snippet_statistics_data(self, play_list_videos, videos_statistics, channel_info):
        all_videos = []
        for video in play_list_videos:
            video_details = self._get_video_details(video['snippet']['resourceId']['videoId'])
            for videos_statistic in videos_statistics:
                if video['snippet']['resourceId']['videoId'] == videos_statistic['id']:
                    combined_data = {**video_details, **videos_statistic['statistics'], **channel_info}
                    all_videos.append(combined_data)

        return all_videos

    @staticmethod
    def encode_to_shiftjis(s: Optional[str]) -> str:
        if s is None:
            return ""
        encoded_str = s.encode("shift_jis", errors="replace").decode("shift_jis")
        return encoded_str

    def save_to_csv(self, video_data_list, csv_path):
        headers = [
            'title', 'description', 'publishedAt', 'thumbnail_url',
            'category', 'tags', 'viewCount', 'likeCount', 'commentCount',
            'favoriteCount', 'channelTitle', 'channelDescription',
            'subscriberCount', 'totalViews', 'totalVideos'
        ]

        # ファイルの存在とサイズをチェック
        file_exists = os.path.exists(csv_path) and os.path.getsize(csv_path) > 0

        with open(csv_path, 'a', newline='', encoding='shift_jis') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)
            for video in video_data_list:
                writer.writerow([
                    YoutubeController.encode_to_shiftjis(video.title),
                    YoutubeController.encode_to_shiftjis(video.description),
                    YoutubeController.encode_to_shiftjis(video.publishedAt),
                    YoutubeController.encode_to_shiftjis(video.thumbnails.default.url),
                    YoutubeController.encode_to_shiftjis(video.category),
                    YoutubeController.encode_to_shiftjis(','.join(video.tags if video.tags else [])),
                    video.viewCount, 
                    video.likeCount,
                    video.commentCount,
                    video.favoriteCount,
                    YoutubeController.encode_to_shiftjis(video.channelTitle),
                    YoutubeController.encode_to_shiftjis(video.channelDescription),
                    video.subscriberCount,
                    video.totalViews,
                    video.totalVideos
                ])

    def reset_csv(self, csv_path):
        """
        Resets the content of the given CSV file.
        """
        # Check if the file exists before trying to clear its content
        if os.path.exists(csv_path):
            # Open the file and immediately close it to clear its content
            open(csv_path, 'w').close()
        else:
            print(f"File {csv_path} does not exist.")
        

if __name__ == "__main__":
    y_ctrl = YoutubeController(api_key=os.environ['api_key'])
    videos = y_ctrl.get_all_videos(youtubech_id=os.environ['ch_id'])
    y_ctrl.save_to_csv(videos, "youtube_videos.csv")
    y_ctrl.reset_csv("youtube_videos.csv")
