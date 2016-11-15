
from django.conf.urls import url

from .views import CommentView

urlpatterns = [
    url(r'^$', CommentView.as_view()),
]
