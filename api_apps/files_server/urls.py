from django.urls import include, path
from django.conf.urls import include, url
from api_apps.files_server.views import stream_video
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

# myobject_slug_detail = myviews.MyObjectViewset.as_view(REQDICT, lookup_field='slug')
# router = routers.DefaultRouter()
# router.register('test/<slug:slug>', my_view)
# router.register(r'source', SpeciesViewSet)
# url_of_view = url(r"^myobjects/(?P<slug>[-\w]+)/$",
#            myobject_slug_detail,
#            name = 'myobject-slug-detail')
urlpatterns = [
   # path('', include(router.urls)),
   url(r'directory/(?P<path>.*)$', stream_video, name='unique_slug'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)