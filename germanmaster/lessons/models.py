"""Darslar modeli - GermanMaster AI."""
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Dars kategoriyalari (Grammatika, Lug'at, Tinglash, va hokazo)."""
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, default="📚", verbose_name="Ikonka")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Asosiy dars modeli."""
    LEVEL_CHOICES = [
        ('A1', 'A1 - Boshlang\'ich'),
        ('A2', 'A2 - Elementar'),
        ('B1', 'B1 - O\'rta'),
        ('B2', 'B2 - Yuqori o\'rta'),
        ('C1', 'C1 - Ilg\'or'),
        ('C2', 'C2 - Professional'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('published', 'Chop etilgan'),
        ('archived', 'Arxivlangan'),
    ]

    title = models.CharField(max_length=200, verbose_name="Dars nomi")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='lessons', verbose_name="Kategoriya"
    )
    level = models.CharField(
        max_length=2, choices=LEVEL_CHOICES,
        default='A1', verbose_name="Daraja"
    )
    description = models.TextField(verbose_name="Qisqacha tavsif")
    content = models.TextField(verbose_name="Dars matni (HTML/Markdown)")
    
    # Multimedia
    pdf_file = models.FileField(
        upload_to='lessons/pdf/', blank=True, null=True,
        verbose_name="PDF fayl"
    )
    video_url = models.URLField(
        blank=True, verbose_name="Video URL (YouTube/Local)"
    )
    video_file = models.FileField(
        upload_to='lessons/video/', blank=True, null=True,
        verbose_name="Video fayl"
    )
    audio_file = models.FileField(
        upload_to='lessons/audio/', blank=True, null=True,
        verbose_name="Audio fayl"
    )
    thumbnail = models.ImageField(
        upload_to='lessons/thumbnails/', blank=True, null=True,
        verbose_name="Dars rasmi"
    )
    
    # Meta
    duration_minutes = models.IntegerField(
        default=30, verbose_name="Davomiyligi (daqiqa)"
    )
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES,
        default='published', verbose_name="Holat"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Tavsiya etilgan")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ['category', 'order', 'created_at']

    def __str__(self):
        return f"[{self.level}] {self.title}"

    @property
    def has_multimedia(self):
        return bool(self.pdf_file or self.video_url or self.video_file or self.audio_file)
