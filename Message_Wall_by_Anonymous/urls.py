from django.conf.urls import patterns, include, url
import settings

urlpatterns = patterns('',
    url(r'^$', 'messages.views.home', name='home'),
    url(r'^write_message/$', 'messages.views.write_message', name='write_message'),
    url(r'^write_review/$', 'messages.views.write_review', name='write_review'),
    url(r'^show_childs_or_tree/$', 'messages.views.show_childs_or_tree', name='show_childs_or_tree'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
