import requests
from django.conf import settings

from posts.models import Comment
from posts.serializer import CommentSerializer


class InstagramClient:
    """Клиент для запросов к Instagram Graph API"""

    def __init__(self):
        self.token = settings.IG_TOKEN
        self.base_url = "https://graph.instagram.com"

    def get_user_posts(self, url: str = None) -> dict:
        """Получить медиа-объекты из Instagram и вернуть JSON"""
    
        if not url:
            url = f"{self.base_url}/me/media"
            params = {
                'fields': 'id,caption,media_type,media_url,timestamp,username,owner,like_count,comments_count',
                'access_token': self.token,
            }
        else:
            params = None

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def create_comment(self, ig_id: str, text: str) -> dict:
        """Создать комментарий через Instagram API"""

        url = f"{self.base_url}/{ig_id}/comments"

        payload = {
            'message': text,
            'access_token': self.token
        }

        response = requests.post(url=url, data=payload)
        response.raise_for_status()
        return response.json()
