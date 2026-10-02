from django.urls import path

from .views import (CategoryListView, CommentCreateView, PostDetailView,
                    PostListView)

urlpatterns = [
    path(
        'posts/',
        PostListView.as_view(),
        name='post-list'
    ),
    path(
        'posts/<uuid:pk>/',
        PostDetailView.as_view(),
        name='post-detail'
    ),
    path(
        'posts/<uuid:pk>/comments/',
        CommentCreateView.as_view(),
        name='comment-create'
    ),
    path(
        'categories/',
        CategoryListView.as_view(),
        name='category-list',
    ),
]