from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Category, Post


class PostTests(APITestCase):
    """Тесты API постов."""

    def test_only_published_posts_are_returned(self):
        Post.objects.create(
            title='Опубликованный пост',
            text='Текст опубликованного поста',
            state=Post.State.PUBLISHED,
        )
        Post.objects.create(
            title='Черновик',
            text='Текст черновика',
            state=Post.State.DRAFT,
        )

        response = self.client.get('/api/posts/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['title'],
            'Опубликованный пост',
        )

    def test_posts_are_filtered_by_category(self):
        python_category = Category.objects.create(
            name='Python',
        )
        django_category = Category.objects.create(
            name='Django',
        )

        python_post = Post.objects.create(
            title='Python',
            text='Python text',
            state=Post.State.PUBLISHED,
        )
        django_post = Post.objects.create(
            title='Django',
            text='Django text',
            state=Post.State.PUBLISHED,
        )

        python_post.categories.add(python_category)
        django_post.categories.add(django_category)

        response = self.client.get(
            f'/api/posts/?category={python_category.id}'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['title'],
            'Python',
        )

    def test_published_post_detail_is_available(self):
        post = Post.objects.create(
            title='Пост',
            text='Текст',
            state=Post.State.PUBLISHED,
        )

        response = self.client.get(
            f'/api/posts/{post.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['title'],
            'Пост',
        )

    def test_draft_post_detail_is_not_available(self):
        post = Post.objects.create(
            title='Черновик',
            text='Текст',
            state=Post.State.DRAFT,
        )

        response = self.client.get(
            f'/api/posts/{post.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_published_at_is_set_automatically(self):
        post = Post.objects.create(
            title='Пост',
            text='Текст',
            state=Post.State.PUBLISHED,
        )

        self.assertIsNotNone(post.published_at)