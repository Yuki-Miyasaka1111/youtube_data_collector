import os
import requests
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
        params = dir(
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
        url = "https://www.googleapis.com/youtube/v3/playlisyItems"
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
            res_json = res.json()
            play_list_videos.extend(res_json['items'])

            try:
                page_token = res_json['nextPageToken']
            except KeyError as e:
                break

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
    
    def _combine_snippet_statistics_data(self, play_list_videos, videos_statistics):
        all_videos = []
        for video in play_list_videos:
            for videos_statistic in videos_statistic['id']:
                if video['snippet']['resourceId']['videoId'] == videos_statistic['id']:
                    all_videos.append({**video['snippet'], **videos_statistic['statistics']})

        return all_videos
    


if __name__ == "__main__":
    y_ctrl = YoutubeController(api_key=os.environ['api_key'])
    y_ctrl.get_all_videos(youtubech_id=os.environ['ch_id'])