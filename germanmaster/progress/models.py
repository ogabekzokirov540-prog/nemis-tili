"""Progress Tracker modeli - GermanMaster AI."""
from django.db import models
from django.utils import timezone
from datetime import timedelta


class DailyProgress(models.Model):
    """Kunlik progress holati."""
    date = models.DateField(unique=True, verbose_name="Sana")
    lessons_completed = models.IntegerField(default=0, verbose_name="Tugatilgan darslar")
    words_learned = models.IntegerField(default=0, verbose_name="O'rganilgan so'zlar")
    words_reviewed = models.IntegerField(default=0, verbose_name="Takrorlangan so'zlar")
    study_minutes = models.IntegerField(default=0, verbose_name="O'qish vaqti (daqiqa)")
    flashcards_reviewed = models.IntegerField(default=0, verbose_name="Flashcard takrorlanganlar")
    notes_created = models.IntegerField(default=0, verbose_name="Yaratilgan eslatmalar")

    class Meta:
        verbose_name = "Kunlik progress"
        verbose_name_plural = "Kunlik progresslar"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.words_learned} so'z, {self.study_minutes} daqiqa"


class LessonProgress(models.Model):
    """Har bir dars uchun progress."""
    STATUS_CHOICES = [
        ('not_started', 'Boshlanmagan'),
        ('in_progress', 'Davom etmoqda'),
        ('completed', 'Tugatilgan'),
    ]

    lesson = models.ForeignKey(
        'lessons.Lesson', on_delete=models.CASCADE,
        related_name='progress_records', verbose_name="Dars"
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES,
        default='not_started', verbose_name="Holat"
    )
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Boshlangan vaqt")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tugatilgan vaqt")
    time_spent_minutes = models.IntegerField(default=0, verbose_name="Sarflangan vaqt (daqiqa)")
    completion_percentage = models.IntegerField(default=0, verbose_name="Tugatilganlik (%)")
    notes = models.TextField(blank=True, verbose_name="Shaxsiy izohlar")

    class Meta:
        verbose_name = "Dars progressi"
        verbose_name_plural = "Dars progresslari"

    def __str__(self):
        return f"{self.lesson.title} - {self.get_status_display()}"


class Streak(models.Model):
    """Kunlik streak (ketma-ket o'qish kunlari)."""
    current_streak = models.IntegerField(default=0, verbose_name="Joriy streak")
    longest_streak = models.IntegerField(default=0, verbose_name="Eng uzun streak")
    last_activity_date = models.DateField(
        null=True, blank=True, verbose_name="Oxirgi faollik sanasi"
    )
    total_study_days = models.IntegerField(default=0, verbose_name="Jami o'qish kunlari")

    class Meta:
        verbose_name = "Streak"
        verbose_name_plural = "Streaklar"

    def update_streak(self):
        """Streak'ni yangilash."""
        today = timezone.now().date()
        
        if self.last_activity_date is None:
            self.current_streak = 1
            self.last_activity_date = today
            self.total_study_days = 1
        elif self.last_activity_date == today:
            pass  # Bugun allaqachon belgilangan
        elif self.last_activity_date == today - timedelta(days=1):
            self.current_streak += 1
            self.last_activity_date = today
            self.total_study_days += 1
        else:
            self.current_streak = 1  # Streak buzildi
            self.last_activity_date = today
            self.total_study_days += 1
        
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        self.save()

    def __str__(self):
        return f"Streak: {self.current_streak} kun (Max: {self.longest_streak})"
