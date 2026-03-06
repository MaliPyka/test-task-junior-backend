from .clients import InstagramClient
from posts.models import Post, Comment


def sync_user_posts() -> list[Post]:
    """Синхронизирует посты пользователя с базой данных."""
    client = InstagramClient()
    url = None
    sync_result = []

    while True:

        data = client.get_user_posts(url=url)

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
                    'comment_count': item.get('comments_count', 0),
                }
            )

            if is_created:
                sync_result.append(post)

        url = data.get('paging', {}).get('next')

        if not url:
            break

    return sync_result


def add_comment_to_post(post, text: str) -> dict:
    """
    Создает комментарий в Instagram API и сохраняет его в бд

    Args:
        post (Post): Объект модели Post, к которому привязывается комментарий
        text (str): Текст комментария

    Возвращает объект класса модели бд Comment
    """

    client = InstagramClient()

    comment_data = client.create_comment(post.instagram_id, text)

    new_comment = Comment.objects.create(
        post=post,
        instagram_id=comment_data.get('id'),
        text=text
    )

    return new_comment
