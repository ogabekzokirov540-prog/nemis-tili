"""Progress Tracker views."""
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import DailyProgress, LessonProgress, Streak


def progress_dashboard(request):
    """Progress dashboard - statistika va grafiklar."""
    today = timezone.now().date()

    # Streak
    streak, _ = Streak.objects.get_or_create(pk=1)

    # Oxirgi 30 kunlik progress
    month_ago = today - timedelta(days=30)
    monthly_progress = DailyProgress.objects.filter(date__gte=month_ago).order_by('date')

    # Haftalik progress
    week_ago = today - timedelta(days=7)
    weekly_progress = DailyProgress.objects.filter(date__gte=week_ago).order_by('date')

    # Umumiy statistika
    from germanmaster.vocabulary.models import Vocabulary
    from germanmaster.lessons.models import Lesson

    total_words = Vocabulary.objects.count()
    learned_words = Vocabulary.objects.filter(srs_level__gte=3).count()
    total_lessons = Lesson.objects.filter(status='published').count()
    completed_lessons = LessonProgress.objects.filter(status='completed').count()

    # Jami o'qish vaqti
    total_study_time = sum(d.study_minutes for d in monthly_progress)

    # Bugungi progress
    daily_progress, _ = DailyProgress.objects.get_or_create(date=today)

    context = {
        'streak': streak,
        'monthly_progress': monthly_progress,
        'weekly_progress': weekly_progress,
        'total_words': total_words,
        'learned_words': learned_words,
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'total_study_time': total_study_time,
        'daily_progress': daily_progress,
        'word_accuracy': round((learned_words / max(total_words, 1)) * 100),
        'lesson_completion': round((completed_lessons / max(total_lessons, 1)) * 100),
    }
    return render(request, 'progress/dashboard.html', context)


def progress_api(request):
    """Progress ma'lumotlarini JSON formatida qaytarish (chart uchun)."""
    days = int(request.GET.get('days', 30))
    today = timezone.now().date()
    start_date = today - timedelta(days=days)

    progress_data = DailyProgress.objects.filter(date__gte=start_date).order_by('date')

    data = {
        'labels': [p.date.strftime('%d/%m') for p in progress_data],
        'words_learned': [p.words_learned for p in progress_data],
        'study_minutes': [p.study_minutes for p in progress_data],
        'flashcards_reviewed': [p.flashcards_reviewed for p in progress_data],
    }
    return JsonResponse(data)
