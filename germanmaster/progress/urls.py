"""Progress URL konfiguratsiyasi."""
from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.progress_dashboard, name='dashboard'),
    path('api/', views.progress_api, name='api'),
]
