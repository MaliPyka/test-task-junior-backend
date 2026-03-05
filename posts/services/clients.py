import requests
from django.conf import settings


class InstagramClient:
    def __init__(self):
        self.token = settings.IG_TOKEN
        self.url = "https://graph.instagram.com/me/media"

    def get_user_posts(self, url: str) -> dict:
        """Получить медиа-объекты из Instagram и вернуть JSON"""
        params = {
            'fields': 'id,caption,media_type,media_url,timestamp,username,owner,like_count,comment_count',
            'access_token': self.token,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
