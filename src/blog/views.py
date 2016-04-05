from .models import Blog
from .serializers import BlogSerializer
from rest_framework import viewsets
from authentication.permissions import IsAdminOrReadOnly


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminOrReadOnly]
