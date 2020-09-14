from rest_framework import generics, views, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from writers.views import message
from blogs.models import Blog
from blogs.serializers import BlogSerializer


class CreateBlogAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        blog = Blog(
            author=get_user_model().objects.get(pk=request.data.get('author')),
            title=request.data.get('title'),
            content=request.data.get('content'),
            is_published=request.data.get('is_published')
        )
        blog.save()
        print(request.data)
        return Response(status=status.HTTP_200_OK)


class ManageBlogAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

class LikeBlogAPI(views.APIView):
    def get(self, request, **kwargs):
        blog = Blog.objects.get(pk=kwargs['blog_pk'])
        user = get_user_model().objects.get(pk=kwargs['user_pk'])
        if user in blog.likes.all():
            blog.likes.remove(user)
            message(user.name + " unliked the blog '{}'".format(blog.title))
        else:
            blog.likes.add(user)
            message(user.name + " liked the blog '{}'".format(blog.title))
        serializer = BlogSerializer(Blog.objects.filter(is_published=True).order_by('-pub_time'), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class SaveBlogAPI(views.APIView):
    pass
