"""AI Features views - Tarjima, kontekst, nutq tanish."""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import TranslationCache, SpeechRecord
import json


@csrf_exempt
@require_POST
def translate_word(request):
    """So'zni tarjima qilish (kesh bilan)."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    text = data.get('text', '').strip()
    source_lang = data.get('source_lang', 'de')
    target_lang = data.get('target_lang', 'uz')

    if not text:
        return JsonResponse({'error': 'Matn kiritilmagan'}, status=400)

    # Keshda borligini tekshirish
    cached = TranslationCache.objects.filter(
        source_text=text,
        source_language=source_lang,
        target_language=target_lang
    ).first()

    if cached:
        return JsonResponse({
            'translation': cached.translated_text,
            'context': cached.context_examples,
            'from_cache': True,
        })

    # Oddiy lug'at asosida tarjima (API mavjud bo'lmasa)
    from germanmaster.vocabulary.models import Vocabulary

    # Ma'lumotlar bazasidan qidirish
    vocab_match = Vocabulary.objects.filter(german_word__iexact=text).first()
    if vocab_match:
        translation = vocab_match.uzbek_translation
        context_examples = vocab_match.example_sentence_de
        if vocab_match.example_sentence_uz:
            context_examples += f"\n{vocab_match.example_sentence_uz}"

        # Keshga saqlash
        TranslationCache.objects.create(
            source_text=text,
            source_language=source_lang,
            target_language=target_lang,
            translated_text=translation,
            context_examples=context_examples,
        )

        return JsonResponse({
            'translation': translation,
            'context': context_examples,
            'gender': vocab_match.gender,
            'plural': vocab_match.plural_form,
            'from_cache': False,
        })

    return JsonResponse({
        'translation': '',
        'context': '',
        'message': 'So\'z bazada topilmadi. Admin paneldan qo\'shing.',
        'from_cache': False,
    })


@csrf_exempt
@require_POST
def get_word_context(request):
    """So'z uchun kontekst va misollar olish."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    word = data.get('word', '').strip()

    if not word:
        return JsonResponse({'error': 'So\'z kiritilmagan'}, status=400)

    from germanmaster.vocabulary.models import Vocabulary

    # So'zni qidirish
    results = Vocabulary.objects.filter(
        german_word__icontains=word
    ).values(
        'german_word', 'uzbek_translation', 'english_translation',
        'gender', 'plural_form', 'example_sentence_de',
        'example_sentence_uz', 'context_note'
    )[:5]

    return JsonResponse({
        'word': word,
        'results': list(results),
        'count': len(results),
    })


def ai_tools(request):
    """AI asboblar sahifasi."""
    recent_translations = TranslationCache.objects.order_by('-created_at')[:10]
    recent_recordings = SpeechRecord.objects.order_by('-created_at')[:5]

    context = {
        'recent_translations': recent_translations,
        'recent_recordings': recent_recordings,
    }
    return render(request, 'ai/tools.html', context)
