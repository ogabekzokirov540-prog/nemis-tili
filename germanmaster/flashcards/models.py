"""Flashcard va SRS modeli - GermanMaster AI."""
from django.db import models
from django.utils import timezone
from datetime import timedelta


class FlashcardDeck(models.Model):
    """Flashcard to'plami (Deck)."""
    name = models.CharField(max_length=200, verbose_name="To'plam nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    lesson = models.ForeignKey(
        'lessons.Lesson', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='flashcard_decks',
        verbose_name="Bog'liq dars"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Flashcard to'plam"
        verbose_name_plural = "Flashcard to'plamlar"

    def __str__(self):
        return self.name

    @property
    def total_cards(self):
        return self.cards.count()

    @property
    def due_cards(self):
        return self.cards.filter(next_review__lte=timezone.now()).count()


class Flashcard(models.Model):
    """Alohida flashcard."""
    deck = models.ForeignKey(
        FlashcardDeck, on_delete=models.CASCADE,
        related_name='cards', verbose_name="To'plam"
    )
    vocabulary = models.ForeignKey(
        'vocabulary.Vocabulary', on_delete=models.CASCADE,
        related_name='flashcards', verbose_name="So'z"
    )
    
    # SRS fields
    ease_factor = models.FloatField(default=2.5, verbose_name="Osonlik koeffitsienti")
    interval_days = models.IntegerField(default=1, verbose_name="Interval (kun)")
    repetitions = models.IntegerField(default=0, verbose_name="Takrorlashlar soni")
    next_review = models.DateTimeField(default=timezone.now, verbose_name="Keyingi takrorlash")
    
    # Stats
    times_correct = models.IntegerField(default=0)
    times_incorrect = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Flashcard"
        verbose_name_plural = "Flashcardlar"
        ordering = ['next_review']

    def __str__(self):
        return f"{self.vocabulary.german_word} ({self.deck.name})"

    def review(self, quality):
        """
        SM-2 algoritmi asosida SRS hisoblash.
        quality: 0-5 (0=umuman bilmaydi, 5=mukammal biladi)
        """
        if quality < 0 or quality > 5:
            return

        # SM-2 Algorithm
        if quality >= 3:  # To'g'ri javob
            if self.repetitions == 0:
                self.interval_days = 1
            elif self.repetitions == 1:
                self.interval_days = 6
            else:
                self.interval_days = round(self.interval_days * self.ease_factor)
            self.repetitions += 1
            self.times_correct += 1
        else:  # Noto'g'ri javob
            self.repetitions = 0
            self.interval_days = 1
            self.times_incorrect += 1

        # Ease factor yangilash
        self.ease_factor = max(1.3, self.ease_factor + (
            0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        ))

        self.next_review = timezone.now() + timedelta(days=self.interval_days)
        self.last_reviewed = timezone.now()
        self.save()


class ReviewSession(models.Model):
    """Har bir takrorlash sessiyasi."""
    deck = models.ForeignKey(
        FlashcardDeck, on_delete=models.CASCADE,
        related_name='sessions', verbose_name="To'plam"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    total_cards = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Takrorlash sessiyasi"
        verbose_name_plural = "Takrorlash sessiyalari"
        ordering = ['-started_at']

    @property
    def accuracy(self):
        total = self.correct_answers + self.incorrect_answers
        if total == 0:
            return 0
        return round((self.correct_answers / total) * 100)

    @property
    def duration_minutes(self):
        if not self.ended_at:
            return 0
        delta = self.ended_at - self.started_at
        return round(delta.total_seconds() / 60)
