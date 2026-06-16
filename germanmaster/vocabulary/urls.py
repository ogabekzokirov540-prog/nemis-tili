"""Lug'at URL konfiguratsiyasi."""
from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    path('', views.vocabulary_list, name='list'),
    path('add/', views.vocabulary_add, name='add'),
    path('<int:pk>/', views.vocabulary_detail, name='detail'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]
