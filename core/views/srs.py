import json
from types import SimpleNamespace
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from core.models import WordLevel, Review, WordReading, WordMeaning, Word
from core.util import get_review_time


@login_required
def show_discover(request):
    return render(request, 'srs/discover.html', {})


def show_review(request):
    return render(request, 'srs/review.html', {})


def get_srs_word_list(word_id_query):
    word_query = (
        Word.objects
        .filter(id__in=word_id_query)
        .values('id', 'word')
    )

    reading_query = (
        WordReading.objects
        .filter(owner_id__in=word_id_query)
        .values('owner_id', 'reading')
    )

    meaning_query = (
        WordMeaning.objects
        .filter(owner_id__in=word_id_query)
        .values('owner_id', 'meaning')
    )

    word_list = {}
    for row in word_query.all():
        word_list[row['id']] = {
            'id': row['id'],
            'word': row['word'],
            'readings': [],
            'meanings': [],
        }

    for reading_row in reading_query.all():
        word_list[reading_row['owner_id']]['readings'].append(reading_row['reading'])

    for meaning_row in meaning_query.all():
        word_list[meaning_row['owner_id']]['meanings'].append(meaning_row['meaning'])

    return list(word_list.values())


@login_required
def get_review_list(request):
    now = timezone.now()
    word_id_query = (
        Review.objects
        .filter(user_id=request.user.id)
        .filter(date__lt=now)
        .values_list('word_id', flat=True)
    )

    word_list = get_srs_word_list(word_id_query)
    return HttpResponse(json.dumps(word_list), content_type="application/json")


# TODO: Limit to 50 elements, then let the app request new words when these words are done.
@login_required
def get_discovery_list(request):
    word_id_query = (
        WordLevel.objects
        .filter(user_id=request.user.id)
        .filter(level=0)
        .values_list('word_id', flat=True)
    )

    discovery_queue = get_srs_word_list(word_id_query)
    return HttpResponse(json.dumps(discovery_queue), content_type="application/json")


@login_required
def finish_discovery(request):
    if request.method == 'PUT':
        word_ids = json.loads(request.body.decode("utf-8"))
        user_word_level_query = WordLevel.objects.filter(user_id=request.user.id)

        affected_row_count = (
            user_word_level_query
                .filter(level=0)
                .filter(word_id__in=word_ids)
                .update(level=1)
        )

        print(affected_row_count)

        if affected_row_count != len(word_ids):
            # In this case at least one word wasn't pushed to level 1,
            # so we need to fetch the words that were.
            word_ids = (
                user_word_level_query
                    .filter(level=1)
                    .filter(word_id__in=word_ids)
                    .values_list('id', flat=True)
                    .all()
            )

        # Insert next reviews.
        review_date = timezone.now() + get_review_time(next_word_level=2)
        Review.objects.bulk_create(
            [Review(word_id=word_id, user_id=request.user.id, date=review_date) for word_id in word_ids]
        )

        return JsonResponse({})
    else:
        return HttpResponseNotFound()


def finish_review(request):
    if request.method == 'PUT':
        user_word_level_query = WordLevel.objects.filter(user_id=request.user.id)

        # Fields: id, meaning_tries, maybe reading_tries (in case the word has kanji)
        stat_data_list = json.loads(request.body.decode("utf-8"))
        word_ids = [stat['id'] for stat in stat_data_list]

        # Transform stats_list into a map.
        stat_map = {}
        for stat_data in stat_data_list:
            wrong_tries = (
                stat_data['meaning_tries'] - 1 +
                stat_data.get('reading_tries', 1) - 1  # In case the word has no kanji, this evaluates to 0.
            )
            # We set level and new_level here to sensible default values, but they should be filled later.
            stat_map[stat_data['id']] = SimpleNamespace(
                word_id=stat_data['id'],
                wrong_tries=wrong_tries,
                level_id=-1,
                level=1,
                new_level=1
            )

        # Fetch current levels.
        word_levels = (
            user_word_level_query
            .filter(word_id__in=word_ids)
            .values_list('id', 'word_id', 'level')
            .all()
        )
        for level_id, word_id, level in word_levels:
            stat = stat_map[word_id]
            stat.level_id = level_id
            stat.level = level

        # Calculate new levels.
        for stat in stat_map.values():
            if stat.wrong_tries > 0:
                stat.new_level = max(1, stat.level - stat.wrong_tries * 2)
            else:
                stat.new_level = min(WordLevel.MAX_LEVEL, stat.level + 1)

        # Delete all reviews for the words.
        print(Review.objects.filter(user_id=request.user.id).filter(word_id__in=word_ids).delete())

        # Update all changed levels in the database and set new review times.
        for stat in stat_map.values():
            if stat.level != stat.new_level:
                WordLevel.objects.filter(id=stat.level_id).update(level=stat.new_level)
            # Review date for the next level.
            review_date = timezone.now() + get_review_time(next_word_level=stat.new_level + 1)
            next_review = Review(user_id=request.user.id, word_id=stat.word_id, date=review_date)
            next_review.save()

        return JsonResponse({})
    else:
        return HttpResponseNotFound()
