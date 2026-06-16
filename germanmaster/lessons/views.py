"""Darslar views - Study Room va darslar ro'yxati."""
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Lesson, Category


def lesson_list(request):
    """Barcha darslar ro'yxati, filter va qidirish bilan."""
    lessons = Lesson.objects.filter(status='published')
    categories = Category.objects.all()

    # Filtrlash
    category_slug = request.GET.get('category')
    level = request.GET.get('level')
    search = request.GET.get('search', '')

    if category_slug:
        lessons = lessons.filter(category__slug=category_slug)
    if level:
        lessons = lessons.filter(level=level)
    if search:
        lessons = lessons.filter(title__icontains=search)

    context = {
        'lessons': lessons,
        'categories': categories,
        'current_category': category_slug,
        'current_level': level,
        'search_query': search,
        'levels': Lesson.LEVEL_CHOICES,
    }
    return render(request, 'lessons/list.html', context)


def study_room(request, slug):
    """Study Room - split-screen dars ko'rish sahifasi."""
    from germanmaster.vocabulary.models import Vocabulary
    from germanmaster.notes.models import Note
    from germanmaster.progress.models import LessonProgress, Streak

    lesson = get_object_or_404(Lesson, slug=slug, status='published')

    # Darsga bog'liq so'zlar
    vocabularies = Vocabulary.objects.filter(lesson=lesson)

    # Darsga bog'liq eslatmalar
    notes = Note.objects.filter(lesson=lesson)

    # Progress yangilash
    progress, created = LessonProgress.objects.get_or_create(lesson=lesson)
    if created or progress.status == 'not_started':
        progress.status = 'in_progress'
        progress.started_at = timezone.now()
        progress.save()

    # Streak yangilash
    streak, _ = Streak.objects.get_or_create(pk=1)
    streak.update_streak()

    # Oldingi va keyingi darslar
    next_lesson = Lesson.objects.filter(
        category=lesson.category, order__gt=lesson.order, status='published'
    ).first()
    prev_lesson = Lesson.objects.filter(
        category=lesson.category, order__lt=lesson.order, status='published'
    ).order_by('-order').first()

    context = {
        'lesson': lesson,
        'vocabularies': vocabularies,
        'notes': notes,
        'progress': progress,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
    }
    return render(request, 'lessons/study_room.html', context)


def complete_lesson(request, slug):
    """Darsni tugatilgan deb belgilash."""
    from germanmaster.progress.models import LessonProgress, DailyProgress
    from django.shortcuts import redirect

    lesson = get_object_or_404(Lesson, slug=slug)
    progress, _ = LessonProgress.objects.get_or_create(lesson=lesson)
    progress.status = 'completed'
    progress.completed_at = timezone.now()
    progress.completion_percentage = 100
    progress.save()

    # Kunlik progress yangilash
    today = timezone.now().date()
    daily, _ = DailyProgress.objects.get_or_create(date=today)
    daily.lessons_completed += 1
    daily.save()

    return redirect('lessons:study_room', slug=slug)
