import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('YT_API_KEY')


class Video:

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id: str):
        self.__video_id = video_id  # id видео
        video_response = self.youtube.videos().list(id=self.__video_id, part='snippet,statistics').execute()

        items = video_response.get('items', [])
        if items:
            video_details = items[0]
            self.video_title = video_details['snippet']['title']  # Название видео
            self.url = 'https://youtu.be/' + video_id  # Ссылка на видео
            self.view_count = video_details['statistics'].get('viewCount', '0')  # Кол-во просмотров
            self.count_likes = video_details['statistics'].get('likeCount', '0')  # Кол-во лайков
        else:
            raise ValueError("No video found with the provided ID")

    def __str__(self):
        return self.video_title


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id = playlist_id
        self.url = f'https://youtu.be/{video_id}?list={playlist_id}'