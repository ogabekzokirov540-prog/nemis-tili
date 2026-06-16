"""Notes URL konfiguratsiyasi."""
from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='list'),
    path('create/', views.note_create, name='create'),
    path('<int:pk>/edit/', views.note_edit, name='edit'),
    path('<int:pk>/delete/', views.note_delete, name='delete'),
    path('<int:pk>/pin/', views.toggle_pin, name='toggle_pin'),
]
