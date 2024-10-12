from django.contrib import admin
from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "content", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ["created_at"]

    def get_ordering(self, request):
        return ["-created_at"]


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "short_content",
        "post",
        "created_at",
        "isActive",
    )
    search_fields = ("name", "email")
    list_per_page = 50
    readonly_fields = ["content"]

    def short_content(self, obj):
        content_words = obj.content.split()[:10]
        return (
            " ".join(content_words) + "..."
            if len(content_words) == 10
            else " ".join(content_words)
        )

    short_content.short_description = "content"
