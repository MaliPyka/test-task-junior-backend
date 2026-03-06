from celery import shared_task

from .services.instagram_service import sync_user_posts


@shared_task
def run_sync_posts() -> str:
    """Выполняет функцию sync_user_posts в фоновом режиме"""
    synced_posts = sync_user_posts()

    return f"Синхронизация окончена! Добавлено новых постов в базу данных: {len(synced_posts)}"



