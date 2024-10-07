from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Post


class PostViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post = Post.objects.create(title="Test Post", content="Test Content")
        self.list_url = reverse("post-list")
        self.detail_url = reverse("post-detail", kwargs={"pk": self.post.pk})

    def test_get_post_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        data = {"title": "New Post", "content": "New Content"}
        response = self.client.post(reverse("create-post"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.post.title)
