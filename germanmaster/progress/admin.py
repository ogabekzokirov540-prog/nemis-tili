"""Progress admin konfiguratsiyasi."""
from django.contrib import admin
from .models import DailyProgress, LessonProgress, Streak


@admin.register(DailyProgress)
class DailyProgressAdmin(admin.ModelAdmin):
    list_display = ['date', 'lessons_completed', 'words_learned', 'words_reviewed', 'study_minutes']
    ordering = ['-date']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'status', 'completion_percentage', 'time_spent_minutes']
    list_filter = ['status']


@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = ['current_streak', 'longest_streak', 'last_activity_date', 'total_study_days']
