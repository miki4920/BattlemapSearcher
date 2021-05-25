from django.conf.urls.static import static

from BattlemapSearcher import settings
from . import views
from . import views_rest
from django.urls import path

app_name = 'mapviewer'


urlpatterns = [
    path('', views.map_tiles, name="map_tiles"),
    path('maps/', views_rest.request_map, name="map_no_parameters"),
    path('maps/<int:map_id>', views_rest.request_map, name="map")]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
