from . import views

app_name = 'mapviewer'

from django.urls import path

urlpatterns = [
    path('maps/', views.map_list),
    path('maps/<int:pk>/', views.map_detail)]