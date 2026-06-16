"""Lug'at (Vocabulary) modeli - GermanMaster AI."""
from django.db import models
from django.utils import timezone


class WordCategory(models.Model):
    """So'z kategoriyalari (Ism, Fe'l, Sifat, va hokazo)."""
    name = models.CharField(max_length=100, verbose_name="Kategoriya")
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default="#3B82F6", verbose_name="Rang (HEX)")

    class Meta:
        verbose_name = "So'z kategoriyasi"
        verbose_name_plural = "So'z kategoriyalari"

    def __str__(self):
        return self.name


class Vocabulary(models.Model):
    """Asosiy so'z modeli - Nemischa lug'at."""
    GENDER_CHOICES = [
        ('der', 'der (Maskulin)'),
        ('die', 'die (Feminin)'),
        ('das', 'das (Neytral)'),
        ('', 'Artikelsiz'),
    ]

    DIFFICULTY_CHOICES = [
        (1, 'Juda oson'),
        (2, 'Oson'),
        (3, 'O\'rtacha'),
        (4, 'Qiyin'),
        (5, 'Juda qiyin'),
    ]

    # Asosiy ma'lumotlar
    german_word = models.CharField(max_length=200, verbose_name="Nemischa so'z")
    uzbek_translation = models.CharField(max_length=200, verbose_name="O'zbekcha tarjima")
    english_translation = models.CharField(
        max_length=200, blank=True, verbose_name="Inglizcha tarjima"
    )
    
    # Grammatika
    gender = models.CharField(
        max_length=3, choices=GENDER_CHOICES,
        blank=True, verbose_name="Artikl (rod)"
    )
    plural_form = models.CharField(
        max_length=200, blank=True, verbose_name="Ko'plik shakli"
    )
    word_type = models.ForeignKey(
        WordCategory, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="So'z turi"
    )
    
    # Kontekst
    example_sentence_de = models.TextField(
        blank=True, verbose_name="Misol gap (nemischa)"
    )
    example_sentence_uz = models.TextField(
        blank=True, verbose_name="Misol gap (o'zbekcha)"
    )
    context_note = models.TextField(
        blank=True, verbose_name="Kontekst/Izoh"
    )
    
    # Multimedia
    image = models.ImageField(
        upload_to='vocabulary/images/', blank=True, null=True,
        verbose_name="Rasm (vizual xotira uchun)"
    )
    audio_pronunciation = models.FileField(
        upload_to='vocabulary/audio/', blank=True, null=True,
        verbose_name="Talaffuz (audio)"
    )
    
    # Bog'lanish
    lesson = models.ForeignKey(
        'lessons.Lesson', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='vocabularies',
        verbose_name="Bog'liq dars"
    )
    
    # SRS (Spaced Repetition System)
    difficulty = models.IntegerField(
        choices=DIFFICULTY_CHOICES, default=3,
        verbose_name="Qiyinlik darajasi"
    )
    srs_level = models.IntegerField(
        default=0, verbose_name="SRS bosqichi (0-5)"
    )
    next_review_date = models.DateTimeField(
        default=timezone.now, verbose_name="Keyingi takrorlash sanasi"
    )
    total_reviews = models.IntegerField(default=0, verbose_name="Jami takrorlashlar")
    correct_reviews = models.IntegerField(default=0, verbose_name="To'g'ri javoblar")
    
    # Tags
    tags = models.CharField(
        max_length=500, blank=True,
        verbose_name="Teglar (vergul bilan ajratilgan)"
    )
    is_favorite = models.BooleanField(default=False, verbose_name="Sevimli")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "So'z"
        verbose_name_plural = "Lug'at"
        ordering = ['-created_at']

    def __str__(self):
        if self.gender:
            return f"{self.gender} {self.german_word} - {self.uzbek_translation}"
        return f"{self.german_word} - {self.uzbek_translation}"

    @property
    def accuracy_percentage(self):
        if self.total_reviews == 0:
            return 0
        return round((self.correct_reviews / self.total_reviews) * 100)

    @property
    def is_due_for_review(self):
        return timezone.now() >= self.next_review_date
