from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'likes_count', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

    def content_preview(self, obj):
        return obj.content[:60]
    content_preview.short_description = 'Content'

    def likes_count(self, obj):
        return obj.get_likes_count()
    likes_count.short_description = 'Likes'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    search_fields = ('author__username', 'content')
