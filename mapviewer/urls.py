from django.conf.urls.static import static

from BattlemapSearcher import settings
from . import views
from django.urls import path

app_name = 'mapviewer'


urlpatterns = [
    path('', views.map_tiles, name="map_tiles"),
    path('maps/', views.request_map, name="map_no_parameters"),
    path('maps/<int:map_id>', views.request_map, name="map")]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
