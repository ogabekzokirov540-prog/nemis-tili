"""GermanMaster AI URL Configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('germanmaster.dashboard.urls')),
    path('lessons/', include('germanmaster.lessons.urls')),
    path('vocabulary/', include('germanmaster.vocabulary.urls')),
    path('flashcards/', include('germanmaster.flashcards.urls')),
    path('notes/', include('germanmaster.notes.urls')),
    path('media-library/', include('germanmaster.media.urls')),
    path('progress/', include('germanmaster.progress.urls')),
    path('ai/', include('germanmaster.ai_features.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
