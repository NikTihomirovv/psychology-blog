import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Модель для описания категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель для описания поста."""

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    class State(models.TextChoices):
        """Описание состояний поста."""
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликован'
        ARCHIVED = 'archived', 'Архивирован'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=300
    )
    description = models.TextField(
        verbose_name='Краткое описание',
        max_length=500,
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Последнее обновление',
        auto_now=True
    )   # Изменить текущее время при каждом сохранении
    published_at = models.DateTimeField(
        verbose_name='Дата публикации',
        null=True,
        blank=True
    )
    state = models.CharField(
        verbose_name='Состояние',
        max_length=20,
        choices=State.choices,
        default=State.DRAFT
    )

    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        blank=True
    )

    def save(self, *args, **kwargs):
        if (
            self.state == self.State.PUBLISHED
            and self.published_at is None
        ):
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class PostImage(models.Model):
    """Модель для описания изображения для поста."""

    class Meta:
        verbose_name = 'Изображение к посту'
        verbose_name_plural = 'Изображения к постам'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Пост',
    )
    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Изображение',
    )

    def __str__(self):
        return f'Изображение для: {self.post}'


class Comment(models.Model):
    """Модель для описания комментария."""

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    is_approved = models.BooleanField(
        verbose_name='Одобрен',
        default=False
    )

    def __str__(self):
        return self.text[:50]


