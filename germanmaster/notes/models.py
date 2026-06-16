"""Smart Note-taking modeli - GermanMaster AI."""
from django.db import models


class Note(models.Model):
    """Darsga bog'liq eslatma/qo'lyozma."""
    title = models.CharField(max_length=300, verbose_name="Eslatma sarlavhasi")
    content = models.TextField(verbose_name="Matn (Markdown qo'llab-quvvatlanadi)")
    
    # Bog'lanish
    lesson = models.ForeignKey(
        'lessons.Lesson', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='notes',
        verbose_name="Bog'liq dars"
    )
    
    # Tags va kategoriya
    tags = models.CharField(max_length=500, blank=True, verbose_name="Teglar")
    color = models.CharField(
        max_length=7, default="#FBBF24",
        verbose_name="Eslatma rangi"
    )
    is_pinned = models.BooleanField(default=False, verbose_name="Qadoqlangan")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Eslatma"
        verbose_name_plural = "Eslatmalar"
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title


class NoteAttachment(models.Model):
    """Eslatmaga biriktirilgan fayllar."""
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE,
        related_name='attachments', verbose_name="Eslatma"
    )
    file = models.FileField(upload_to='notes/attachments/', verbose_name="Fayl")
    file_name = models.CharField(max_length=300, verbose_name="Fayl nomi")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Biriktirma"
        verbose_name_plural = "Biriktirmalar"

    def __str__(self):
        return self.file_name
