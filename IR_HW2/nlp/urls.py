from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home),
    path('handle_content', views.handle_content),
    path('partial_matching', views.partial_matching),
    path('search', views.search_keyword),
]