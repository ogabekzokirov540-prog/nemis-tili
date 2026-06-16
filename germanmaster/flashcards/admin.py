"""Flashcards admin konfiguratsiyasi."""
from django.contrib import admin
from .models import FlashcardDeck, Flashcard, ReviewSession


@admin.register(FlashcardDeck)
class FlashcardDeckAdmin(admin.ModelAdmin):
    list_display = ['name', 'lesson', 'total_cards', 'due_cards', 'is_active', 'created_at']
    list_filter = ['is_active', 'lesson']
    search_fields = ['name', 'description']


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['vocabulary', 'deck', 'interval_days', 'repetitions', 'next_review']
    list_filter = ['deck', 'repetitions']
    ordering = ['next_review']


@admin.register(ReviewSession)
class ReviewSessionAdmin(admin.ModelAdmin):
    list_display = ['deck', 'total_cards', 'correct_answers', 'incorrect_answers', 'accuracy', 'started_at']
    list_filter = ['deck']
    ordering = ['-started_at']
