from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from posts.models import Post
from posts.services.instagram_service import add_comment_to_post
from .serializer import CommentSerializer, PostSerializer
from .pagination import PostCursorPagination
from .tasks import run_sync_posts


class SyncPostView(APIView):
    """Эндпоинт для синхронизации медиа-объектов"""

    def post(self, request):
        try:
            run_sync_posts.delay()
            return Response(
                {"message": "Синхронизация запущена!"},
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(
                {
                    "message": "Не удалось запустить синхронизацию!",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination

    @action(detail=True, methods=['post'], serializer_class=CommentSerializer)
    def comment(self, request, pk=None):
        """
        Эндпоинт для добавления комментария к конкретному посту.
        Ожидает JSON: {"text": "сообщение"}
        """

        post = self.get_object()

        text = request.data.get('text')

        try:
            comment = add_comment_to_post(post, text)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "error", "detail": str(e)}, status.HTTP_400_BAD_REQUEST)
