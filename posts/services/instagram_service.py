from .clients import InstagramClient
from posts.models import Post


def sync_user_posts() -> list[Post]:
    """Синхронизировать посты пользователя с базой данных."""
    client = InstagramClient()
    url = client.url
    sync_result = []

    while url:

        data = client.get_user_posts(url)

        for item in data.get('data', []):
            post, is_created = Post.objects.update_or_create(
                instagram_id=item.get('id'),
                defaults={
                    'username': item.get('username'),
                    'owner': item.get('owner', {}).get('id'),
                    'caption': item.get('caption', ''),
                    'media_type': item.get('media_type'),
                    'media_url': item.get('media_url'),
                    'timestamp': item.get('timestamp'),
                    'like_count': item.get('like_count', 0),
                    'comment_count': item.get('comment_count', 0),
                }
            )

            if is_created:
                sync_result.append(post)

        url = data.get('paging', {}).get('next')

    return sync_result
