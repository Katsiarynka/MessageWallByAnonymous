
from django.conf.urls import url, include
from rest_framework import routers

from comments.views import CommentViewSet


router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
