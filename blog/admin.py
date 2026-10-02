from django.contrib import admin

from .models import Category, Comment, Post, PostImage


class PostImageInline(admin.TabularInline):
    """Изображения поста в Django Admin."""

    model = PostImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройка постов в Django Admin."""

    list_display = (
        'title',
        'state',
        'created_at',
        'published_at',
    )
    list_filter = (
        'state',
        'categories',
    )
    search_fields = (
        'title',
        'description',
        'text',
    )
    filter_horizontal = (
        'categories',
    )
    inlines = (
        PostImageInline,
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка комментариев в Django Admin."""

    list_display = (
        'author',
        'post',
        'created_at',
        'is_approved',
    )
    list_filter = (
        'is_approved',
    )
    search_fields = (
        'text',
    )
    actions = (
        'approve_comments',
    )

    @admin.action(description='Одобрить выбранные комментарии')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)


admin.site.register(Category)