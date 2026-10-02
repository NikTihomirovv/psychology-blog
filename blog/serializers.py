from rest_framework import serializers

from .models import Category, Comment, Post, PostImage


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )


class PostImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображения поста."""

    class Meta:
        model = PostImage
        fields = (
            'id',
            'image',
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментария."""

    author = serializers.CharField(
        source='author.username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'created_at',
        )
        read_only_fields = (
            'id',
            'author',
            'created_at',
        )

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'Комментарий не может состоять только из пробелов.'
            )

        return value


class PostListSerializer(serializers.ModelSerializer):
    """Сериализатор списка постов."""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'description',
            'image',
            'published_at',
        )

    def get_image(self, obj):
        images = list(obj.images.all())

        if not images:
            return None

        return images[0].image.url


class PostDetailSerializer(serializers.ModelSerializer):
    """Сериализатор детальной информации о посте."""

    categories = CategorySerializer(
        many=True,
        read_only=True,
    )
    images = PostImageSerializer(
        many=True,
        read_only=True,
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'text',
            'created_at',
            'published_at',
            'state',
            'categories',
            'images',
            'comments'
        )

    def get_comments(self, obj):
        return CommentSerializer(
            obj.approved_comments,
            many=True,
        ).data