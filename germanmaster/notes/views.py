"""Smart Notes views."""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Note, NoteAttachment


def note_list(request):
    """Barcha eslatmalar ro'yxati."""
    notes = Note.objects.all()

    # Filtrlash
    search = request.GET.get('search', '')
    lesson_id = request.GET.get('lesson')
    pinned_only = request.GET.get('pinned')

    if search:
        notes = notes.filter(title__icontains=search) | notes.filter(content__icontains=search)
    if lesson_id:
        notes = notes.filter(lesson_id=lesson_id)
    if pinned_only:
        notes = notes.filter(is_pinned=True)

    from germanmaster.lessons.models import Lesson
    context = {
        'notes': notes,
        'lessons': Lesson.objects.filter(status='published'),
        'search_query': search,
    }
    return render(request, 'notes/list.html', context)


def note_create(request):
    """Yangi eslatma yaratish."""
    if request.method == 'POST':
        note = Note(
            title=request.POST.get('title', ''),
            content=request.POST.get('content', ''),
            tags=request.POST.get('tags', ''),
            color=request.POST.get('color', '#FBBF24'),
            is_pinned=request.POST.get('is_pinned') == 'on',
        )
        if request.POST.get('lesson_id'):
            note.lesson_id = int(request.POST['lesson_id'])
        note.save()

        # Fayllarni biriktirish
        for f in request.FILES.getlist('attachments'):
            NoteAttachment.objects.create(
                note=note, file=f, file_name=f.name
            )

        # Kunlik progress
        from germanmaster.progress.models import DailyProgress
        today = timezone.now().date()
        daily, _ = DailyProgress.objects.get_or_create(date=today)
        daily.notes_created += 1
        daily.save()

        return redirect('notes:list')

    from germanmaster.lessons.models import Lesson
    context = {
        'lessons': Lesson.objects.filter(status='published'),
    }
    return render(request, 'notes/create.html', context)


def note_edit(request, pk):
    """Eslatmani tahrirlash."""
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        note.title = request.POST.get('title', note.title)
        note.content = request.POST.get('content', note.content)
        note.tags = request.POST.get('tags', note.tags)
        note.color = request.POST.get('color', note.color)
        note.is_pinned = request.POST.get('is_pinned') == 'on'
        if request.POST.get('lesson_id'):
            note.lesson_id = int(request.POST['lesson_id'])
        else:
            note.lesson_id = None
        note.save()

        # Yangi fayllar
        for f in request.FILES.getlist('attachments'):
            NoteAttachment.objects.create(
                note=note, file=f, file_name=f.name
            )

        return redirect('notes:list')

    from germanmaster.lessons.models import Lesson
    context = {
        'note': note,
        'lessons': Lesson.objects.filter(status='published'),
    }
    return render(request, 'notes/edit.html', context)


@require_POST
def note_delete(request, pk):
    """Eslatmani o'chirish."""
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect('notes:list')


@require_POST
def toggle_pin(request, pk):
    """Eslatmani pin/unpin qilish (AJAX)."""
    note = get_object_or_404(Note, pk=pk)
    note.is_pinned = not note.is_pinned
    note.save()
    return JsonResponse({'status': 'ok', 'is_pinned': note.is_pinned})
