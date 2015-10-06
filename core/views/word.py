from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from core.models import Word, WordReading, WordMeaning, WordLevel
from core.util import get_known_kanji_set


@login_required
def word_detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    readings = WordReading.objects.filter(owner=word).values_list('reading', flat=True).all()
    meanings = WordMeaning.objects.filter(owner=word).values_list('meaning', flat=True).all()
    known_kanij = get_known_kanji_set(request.user.id, word.kanji_dependencies.get_queryset())
    level = WordLevel.objects.filter(user_id=request.user.id, word=word).first()
    if level is None:
        level = -1
    else:
        level = level.level
    return render(request, 'word/detail.html', {
        'word': word,
        'kanji_list': word.kanji_dependencies.all(),
        'known_kanji_set': known_kanij,
        'readings': ', '.join(readings),
        'meanings': ', '.join(meanings),
        'level': level,
        'max_level': WordLevel.MAX_LEVEL,
    })


@login_required
def word_list(request):
    words = Word.objects.all()
    return render(request, 'word/list.html', {'words': words})