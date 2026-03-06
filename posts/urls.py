from django.urls import include
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from .views import SyncPostView, PostViewSet

router = DefaultRouter()

router.register(prefix=r'',viewset=PostViewSet,basename='post')

urlpatterns = [
    path('sync/', SyncPostView.as_view(), name='sync_posts'),
    path('posts/', include(router.urls))
]
