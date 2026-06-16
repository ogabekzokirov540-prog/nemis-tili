"""AI Features URL konfiguratsiyasi."""
from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('', views.ai_tools, name='tools'),
    path('translate/', views.translate_word, name='translate'),
    path('context/', views.get_word_context, name='context'),
]
