"""Flashcards URL konfiguratsiyasi."""
from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.deck_list, name='deck_list'),
    path('quick-review/', views.quick_review, name='quick_review'),
    path('deck/<int:deck_id>/review/', views.review_session, name='review'),
    path('card/<int:card_id>/review/', views.review_card, name='review_card'),
    path('session/<int:session_id>/end/', views.end_session, name='end_session'),
]
