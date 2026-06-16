"""Flashcards views - SRS asosida takrorlash."""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import FlashcardDeck, Flashcard, ReviewSession


def deck_list(request):
    """Barcha flashcard to'plamlar."""
    decks = FlashcardDeck.objects.filter(is_active=True)
    total_due = Flashcard.objects.filter(next_review__lte=timezone.now()).count()

    context = {
        'decks': decks,
        'total_due': total_due,
    }
    return render(request, 'flashcards/deck_list.html', context)


def review_session(request, deck_id):
    """Flashcard takrorlash sessiyasi."""
    deck = get_object_or_404(FlashcardDeck, pk=deck_id, is_active=True)

    # Takrorlashga tayyor kartalar
    due_cards = Flashcard.objects.filter(
        deck=deck, next_review__lte=timezone.now()
    ).select_related('vocabulary')[:20]  # Bir sessiyada max 20 ta

    # Sessiya yaratish
    session = ReviewSession.objects.create(
        deck=deck,
        total_cards=due_cards.count()
    )

    context = {
        'deck': deck,
        'cards': list(due_cards.values(
            'id', 'vocabulary__german_word', 'vocabulary__uzbek_translation',
            'vocabulary__gender', 'vocabulary__example_sentence_de',
            'vocabulary__image', 'vocabulary__audio_pronunciation',
            'interval_days', 'repetitions'
        )),
        'session_id': session.id,
        'total_due': due_cards.count(),
    }
    return render(request, 'flashcards/review.html', context)


@require_POST
def review_card(request, card_id):
    """Flashcard javobini qayta ishlash (AJAX)."""
    from germanmaster.progress.models import DailyProgress

    card = get_object_or_404(Flashcard, pk=card_id)
    quality = int(request.POST.get('quality', 0))

    # SM-2 algoritmi bilan yangilash
    card.review(quality)

    # Kunlik progress yangilash
    today = timezone.now().date()
    daily, _ = DailyProgress.objects.get_or_create(date=today)
    daily.flashcards_reviewed += 1
    if quality >= 3:
        daily.words_reviewed += 1
    daily.save()

    # Vocabulary SRS ham yangilash
    vocab = card.vocabulary
    vocab.total_reviews += 1
    vocab.last_reviewed_at = timezone.now()
    if quality >= 3:
        vocab.correct_reviews += 1
        vocab.srs_level = min(5, vocab.srs_level + 1)
    else:
        vocab.srs_level = max(0, vocab.srs_level - 1)
    vocab.save()

    return JsonResponse({
        'status': 'ok',
        'new_interval': card.interval_days,
        'next_review': card.next_review.strftime('%Y-%m-%d'),
    })


@require_POST
def end_session(request, session_id):
    """Sessiyani tugatish."""
    session = get_object_or_404(ReviewSession, pk=session_id)
    session.ended_at = timezone.now()
    session.correct_answers = int(request.POST.get('correct', 0))
    session.incorrect_answers = int(request.POST.get('incorrect', 0))
    session.save()
    return JsonResponse({'status': 'ok', 'accuracy': session.accuracy})


def quick_review(request):
    """Tezkor takrorlash - barcha to'plamlardan due kartalar."""
    due_cards = Flashcard.objects.filter(
        next_review__lte=timezone.now()
    ).select_related('vocabulary', 'deck')[:20]

    context = {
        'cards': list(due_cards.values(
            'id', 'vocabulary__german_word', 'vocabulary__uzbek_translation',
            'vocabulary__gender', 'vocabulary__example_sentence_de',
            'vocabulary__image', 'vocabulary__audio_pronunciation',
            'deck__name', 'interval_days', 'repetitions'
        )),
        'total_due': due_cards.count(),
    }
    return render(request, 'flashcards/quick_review.html', context)
