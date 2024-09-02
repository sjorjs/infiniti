from django.urls import path
from blog.views import CreatePost, PostList

urlpatterns = [
    path('create/post/', CreatePost.as_view(), name='create-post'),
    path('posts/', PostList.as_view(), name='post-list'),
]
