from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for class Comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_fields = ['id', 'created', 'node_history', 'parent']
    search_fields = ['id', 'text', 'created', 'updated', 'node_history', 'parent']
