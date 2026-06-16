"""Dashboard views - Bosh sahifa."""
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta


def dashboard_home(request):
    """Asosiy dashboard sahifasi."""
    from germanmaster.lessons.models import Lesson
    from germanmaster.vocabulary.models import Vocabulary
    from germanmaster.progress.models import DailyProgress, Streak, LessonProgress
    from germanmaster.flashcards.models import Flashcard

    # Oxirgi darslar
    recent_lessons = Lesson.objects.filter(status='published').order_by('-created_at')[:5]

    # Bugungi progress
    today = timezone.now().date()
    daily_progress, _ = DailyProgress.objects.get_or_create(date=today)

    # Streak
    streak, _ = Streak.objects.get_or_create(pk=1)

    # Statistikalar
    total_words = Vocabulary.objects.count()
    learned_words = Vocabulary.objects.filter(srs_level__gte=3).count()
    due_flashcards = Flashcard.objects.filter(next_review__lte=timezone.now()).count()
    completed_lessons = LessonProgress.objects.filter(status='completed').count()
    total_lessons = Lesson.objects.filter(status='published').count()

    # Haftalik progress (oxirgi 7 kun)
    week_ago = today - timedelta(days=7)
    weekly_progress = DailyProgress.objects.filter(date__gte=week_ago).order_by('date')

    context = {
        'recent_lessons': recent_lessons,
        'daily_progress': daily_progress,
        'streak': streak,
        'total_words': total_words,
        'learned_words': learned_words,
        'due_flashcards': due_flashcards,
        'completed_lessons': completed_lessons,
        'total_lessons': total_lessons,
        'weekly_progress': weekly_progress,
    }
    return render(request, 'dashboard/home.html', context)
