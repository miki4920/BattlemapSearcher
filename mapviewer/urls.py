from django.conf.urls.static import static

from BattlemapSearcher import settings
from . import views

app_name = 'mapviewer'

from django.urls import path

urlpatterns = [
    path('maps/', views.MapUpload.as_view(), name="map_uploader"),
    path('', views.index, name="map_viewer")]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)