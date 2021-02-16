from . import views

app_name = 'mapviewer'

from django.urls import path

urlpatterns = [
    path('maps/', views.MapUpload.as_view())]