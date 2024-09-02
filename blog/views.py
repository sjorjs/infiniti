from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from blog.models import Post
from blog.serializers import PostSerializer


class CreatePost(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']

    # serializer_class = PostSerializer
    #
    # def get_queryset(self):
    #     queryset = Post.objects.all()
    #     search_query = self.request.query_params.get('search', None)
    #     if search_query:
    #         queryset = queryset.filter(title__icontains=search_query)
    #     return queryset


class PostDetail(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
