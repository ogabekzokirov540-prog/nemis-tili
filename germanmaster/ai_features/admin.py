"""AI Features admin konfiguratsiyasi."""
from django.contrib import admin
from .models import TranslationCache, SpeechRecord


@admin.register(TranslationCache)
class TranslationCacheAdmin(admin.ModelAdmin):
    list_display = ['source_text', 'source_language', 'target_language', 'created_at']
    list_filter = ['source_language', 'target_language']
    search_fields = ['source_text', 'translated_text']


@admin.register(SpeechRecord)
class SpeechRecordAdmin(admin.ModelAdmin):
    list_display = ['transcribed_text', 'accuracy_score', 'created_at']
    ordering = ['-created_at']
