from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from .models import Post, Comment


class PostAPITest(APITestCase):
    """Тестирование эндпоинтов для работы с постами и комментариями"""

    def setUp(self):
        """Создание тестового поста для использования в тестах"""
        self.post = Post.objects.create(
            owner="roma",
            media_type="image",
            instagram_id="test_ig_123",
            media_url="https://scontent.cdninstagram.com/v/t51.82787-15/test.jpg",
            caption="Test Post",
            username="Test",
            timestamp=timezone.now()
        )
        self.url = f'/api/posts/{self.post.id}/comment/'

    @patch('posts.services.instagram_service.InstagramClient.create_comment')
    def test_create_comment_success(self, mock_create):
        """Проверка успешного создания комментария в бд и корректного ответа"""
        mock_create.return_value = {'id': '2342643636'}

        payload = {'text': 'Тестовый комментарий'}
        response = self.client.post(self.url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'Тестовый комментарий')
        self.assertEqual(Comment.objects.count(), 1)
        
        created_comment = Comment.objects.first()
        self.assertEqual(created_comment.instagram_id, '2342643636')
        self.assertEqual(created_comment.post, self.post)

    def test_create_comment_post_not_found_in_db(self):
        """Проверка ошибки 404, если ID поста не существует в базе данных"""
        bad_url = '/api/posts/2254/comment/'
        payload = {'text': 'Тестовый комментарий'}

        response = self.client.post(bad_url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.count(), 0)

    @patch('posts.services.instagram_service.InstagramClient.create_comment')
    def test_create_comment_missing_in_instagram(self, mock_create):
        """Проверка ошибки 400, если API Instagram вернуло ошибку"""
        mock_create.side_effect = Exception("Instagram API упал")

        payload = {'text': 'Тестовый комментарий'}
        response = self.client.post(self.url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)