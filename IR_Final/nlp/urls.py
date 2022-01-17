from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home),
    path('search', views.search_docs),
    path('handle_content', views.handle_content)
]