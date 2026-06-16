"""Lug'at admin konfiguratsiyasi."""
from django.contrib import admin
from .models import WordCategory, Vocabulary


@admin.register(WordCategory)
class WordCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = [
        'german_word', 'gender', 'uzbek_translation',
        'word_type', 'difficulty', 'srs_level', 'is_favorite'
    ]
    list_filter = ['gender', 'word_type', 'difficulty', 'srs_level', 'is_favorite', 'lesson']
    search_fields = ['german_word', 'uzbek_translation', 'english_translation', 'tags']
    list_editable = ['difficulty', 'is_favorite']
    ordering = ['-created_at']
    fieldsets = (
        ('Asosiy', {
            'fields': ('german_word', 'uzbek_translation', 'english_translation', 'gender', 'plural_form', 'word_type')
        }),
        ('Kontekst', {
            'fields': ('example_sentence_de', 'example_sentence_uz', 'context_note', 'tags'),
        }),
        ('Multimedia', {
            'fields': ('image', 'audio_pronunciation'),
            'classes': ('collapse',),
        }),
        ('Bog\'lanish va SRS', {
            'fields': ('lesson', 'difficulty', 'srs_level', 'next_review_date', 'is_favorite'),
        }),
    )
