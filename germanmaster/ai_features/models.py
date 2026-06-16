"""AI Features modeli - GermanMaster AI."""
from django.db import models


class TranslationCache(models.Model):
    """Tarjimalar keshi - API chaqiruvlarni kamaytirish uchun."""
    source_text = models.TextField(verbose_name="Asl matn")
    source_language = models.CharField(max_length=5, default='de', verbose_name="Manba til")
    target_language = models.CharField(max_length=5, default='uz', verbose_name="Maqsad til")
    translated_text = models.TextField(verbose_name="Tarjima")
    context_examples = models.TextField(blank=True, verbose_name="Kontekst misollari")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tarjima kesh"
        verbose_name_plural = "Tarjima keshlar"
        unique_together = ['source_text', 'source_language', 'target_language']

    def __str__(self):
        return f"{self.source_text[:50]} → {self.translated_text[:50]}"


class SpeechRecord(models.Model):
    """Audio-to-Text yozuvlari."""
    audio_file = models.FileField(
        upload_to='speech/recordings/', verbose_name="Audio yozuv"
    )
    transcribed_text = models.TextField(blank=True, verbose_name="Aniqlangan matn")
    expected_text = models.TextField(blank=True, verbose_name="Kutilgan matn")
    accuracy_score = models.FloatField(
        null=True, blank=True, verbose_name="Aniqlik balli (%)"
    )
    feedback = models.TextField(blank=True, verbose_name="AI tavsiyalari")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Nutq yozuvi"
        verbose_name_plural = "Nutq yozuvlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"Yozuv: {self.transcribed_text[:50]}..."
