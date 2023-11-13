import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


class Channel:
    """Класс для ютуб-канала"""
    load_dotenv()
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{channel["items"][0]["id"]}'
        self.subscribe_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, filename):
        json_dict = {
            'channel_id': self.channel_id,
            'title': self.description,
            'description': self.description,
            'url': self.url,
            'subscriberCount': self.subscribe_count,
            'videoCount': self.video_count,
            'viewCount': self.view_count
        }
        with open(filename, 'w') as file:
            json.dump(json_dict, file)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        to_json = json.dumps(channel, indent=2, ensure_ascii=False)
        print(to_json)
        return to_json
