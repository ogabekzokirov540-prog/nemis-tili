"""Notes admin konfiguratsiyasi."""
from django.contrib import admin
from .models import Note, NoteAttachment


class NoteAttachmentInline(admin.TabularInline):
    model = NoteAttachment
    extra = 1


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'is_pinned', 'color', 'updated_at']
    list_filter = ['is_pinned', 'lesson']
    search_fields = ['title', 'content', 'tags']
    list_editable = ['is_pinned']
    inlines = [NoteAttachmentInline]
