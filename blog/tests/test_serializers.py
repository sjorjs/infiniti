from django.test import TestCase
from blog.serializers import PostSerializer
from blog.models import Post


class PostSerializerTest(TestCase):
    def setUp(self):
        self.post_attributes = {
            "title": "Test Post",
            "content": "This is test post content",
        }
        self.post = Post.objects.create(**self.post_attributes)
        self.serializer = PostSerializer(instance=self.post)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "title", "content", "created_at", "updated_at"]),
        )

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["title"], self.post_attributes["title"])
        self.assertEqual(data["content"], self.post_attributes["content"])
