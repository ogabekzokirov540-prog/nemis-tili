"""Darslar URL konfiguratsiyasi."""
from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lesson_list, name='list'),
    path('<slug:slug>/', views.study_room, name='study_room'),
    path('<slug:slug>/complete/', views.complete_lesson, name='complete'),
]
