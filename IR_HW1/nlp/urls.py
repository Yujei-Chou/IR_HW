from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home),
    path('upload', views.handle_uploadFiles),
]