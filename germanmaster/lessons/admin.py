"""Darslar admin konfiguratsiyasi."""
from django.contrib import admin
from .models import Category, Lesson


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'level', 'status', 'is_featured', 'duration_minutes', 'created_at']
    list_filter = ['category', 'level', 'status', 'is_featured']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured', 'level']
    ordering = ['category', 'order']
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'category', 'level', 'description', 'content')
        }),
        ('Multimedia', {
            'fields': ('pdf_file', 'video_url', 'video_file', 'audio_file', 'thumbnail'),
            'classes': ('collapse',),
        }),
        ('Sozlamalar', {
            'fields': ('duration_minutes', 'order', 'status', 'is_featured'),
        }),
    )
