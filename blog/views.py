from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Category, Comment, Post
from .serializers import (CategorySerializer, CommentSerializer,
                          PostDetailSerializer, PostListSerializer)


class CategoryListView(ListAPIView):
    """Получение списка категорий."""

    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer


class PostListView(ListAPIView):
    """Получение списка опубликованных постов."""

    serializer_class = PostListSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(
            state=Post.State.PUBLISHED
        ).prefetch_related(
            'images',
        ).order_by('-published_at')

        category = self.request.query_params.get('category')

        if category:
            queryset = queryset.filter(
                categories__id=category
            )

        return queryset


class PostDetailView(RetrieveAPIView):
    """Получение опубликованного поста по идентификатору."""

    queryset = Post.objects.filter(
        state=Post.State.PUBLISHED
    ).prefetch_related(
        'categories',
        'images',
        Prefetch(
            'comments',
            queryset=Comment.objects.filter(
                is_approved=True
            ).select_related('author'),
            to_attr='approved_comments',
        ),
    )

    serializer_class = PostDetailSerializer


class CommentCreateView(CreateAPIView):
    """Создание комментария к посту."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            pk=self.kwargs['pk'],
            state=Post.State.PUBLISHED,
        )
        serializer.save(
            author=self.request.user,
            post=post
        )