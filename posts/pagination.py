from rest_framework.pagination import CursorPagination


class PostCursorPagination(CursorPagination):
    "Настройка пагинации для отображения списка постов пользователя"

    page_size = 10
    ordering = "-timestamp"
