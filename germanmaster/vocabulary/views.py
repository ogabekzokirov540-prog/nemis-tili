"""Lug'at views."""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Vocabulary, WordCategory


def vocabulary_list(request):
    """Barcha so'zlar ro'yxati."""
    words = Vocabulary.objects.all()
    categories = WordCategory.objects.all()

    # Filtrlash
    category_id = request.GET.get('category')
    gender = request.GET.get('gender')
    search = request.GET.get('search', '')
    favorites_only = request.GET.get('favorites')

    if category_id:
        words = words.filter(word_type_id=category_id)
    if gender:
        words = words.filter(gender=gender)
    if search:
        words = words.filter(german_word__icontains=search) | words.filter(uzbek_translation__icontains=search)
    if favorites_only:
        words = words.filter(is_favorite=True)

    context = {
        'words': words,
        'categories': categories,
        'search_query': search,
        'total_count': words.count(),
    }
    return render(request, 'vocabulary/list.html', context)


def vocabulary_detail(request, pk):
    """So'z tafsilotlari."""
    word = get_object_or_404(Vocabulary, pk=pk)
    context = {'word': word}
    return render(request, 'vocabulary/detail.html', context)


@require_POST
def toggle_favorite(request, pk):
    """So'zni sevimli qilish/olib tashlash (AJAX)."""
    word = get_object_or_404(Vocabulary, pk=pk)
    word.is_favorite = not word.is_favorite
    word.save()
    return JsonResponse({'status': 'ok', 'is_favorite': word.is_favorite})


def vocabulary_add(request):
    """Yangi so'z qo'shish."""
    from django.shortcuts import redirect

    if request.method == 'POST':
        word = Vocabulary(
            german_word=request.POST.get('german_word', ''),
            uzbek_translation=request.POST.get('uzbek_translation', ''),
            english_translation=request.POST.get('english_translation', ''),
            gender=request.POST.get('gender', ''),
            plural_form=request.POST.get('plural_form', ''),
            example_sentence_de=request.POST.get('example_de', ''),
            example_sentence_uz=request.POST.get('example_uz', ''),
            context_note=request.POST.get('context_note', ''),
            difficulty=int(request.POST.get('difficulty', 3)),
            tags=request.POST.get('tags', ''),
        )
        if request.POST.get('lesson_id'):
            word.lesson_id = int(request.POST['lesson_id'])
        if request.POST.get('word_type_id'):
            word.word_type_id = int(request.POST['word_type_id'])
        if request.FILES.get('image'):
            word.image = request.FILES['image']
        if request.FILES.get('audio'):
            word.audio_pronunciation = request.FILES['audio']
        word.save()
        return redirect('vocabulary:list')

    from germanmaster.lessons.models import Lesson
    context = {
        'categories': WordCategory.objects.all(),
        'lessons': Lesson.objects.filter(status='published'),
    }
    return render(request, 'vocabulary/add.html', context)
