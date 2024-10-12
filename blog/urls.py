from django.urls import path
from blog.views import CreatePost, PostList, PostDetail, Comments

urlpatterns = [
    path("create/post/", CreatePost.as_view(), name="create-post"),
    path("posts/", PostList.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("comments/", Comments.as_view(), name="comments"),
]
