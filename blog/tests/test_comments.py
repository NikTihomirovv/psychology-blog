from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Comment, Post

User = get_user_model()


class CommentTests(APITestCase):
    """Тесты API комментариев."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )
        self.post = Post.objects.create(
            title='Опубликованный пост',
            text='Текст',
            state=Post.State.PUBLISHED,
        )

    def test_anonymous_user_cannot_create_comment(self):
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            {
                'text': 'Комментарий',
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(Comment.objects.count(), 0)

    def test_authenticated_user_can_create_comment(self):
        self.client.force_authenticate(
            user=self.user,
        )

        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            {
                'text': 'Комментарий',
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_author_is_current_user(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            {
                'text': 'Комментарий',
            },
        )

        comment = Comment.objects.get()

        self.assertEqual(
            comment.author,
            self.user,
        )

    def test_new_comment_is_not_approved(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            {
                'text': 'Комментарий',
            },
        )

        comment = Comment.objects.get()

        self.assertFalse(comment.is_approved)

    def test_unapproved_comment_is_not_public(self):
        Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Скрытый комментарий',
            is_approved=False,
        )

        response = self.client.get(
            f'/api/posts/{self.post.id}/'
        )

        self.assertEqual(
            response.data['comments'],
            [],
        )

    def test_approved_comment_is_public(self):
        Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Одобренный комментарий',
            is_approved=True,
        )

        response = self.client.get(
            f'/api/posts/{self.post.id}/'
        )

        self.assertEqual(
            len(response.data['comments']),
            1,
        )
        self.assertEqual(
            response.data['comments'][0]['text'],
            'Одобренный комментарий',
        )

    def test_comment_cannot_be_created_for_draft(self):
        draft = Post.objects.create(
            title='Черновик',
            text='Текст',
            state=Post.State.DRAFT,
        )

        self.client.force_authenticate(
            user=self.user,
        )

        response = self.client.post(
            f'/api/posts/{draft.id}/comments/',
            {
                'text': 'Комментарий',
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(Comment.objects.count(), 0)