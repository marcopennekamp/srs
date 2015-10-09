from datetime import timedelta
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from core.models import WordLevel, Review, WordReading, WordMeaning, Word


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


# Returns the time in seconds to the next review.
def get_review_time(next_word_level):
    minutes = 60
    hours = 60 * minutes
    days = 24 * hours
    level_to_time = [
        0,                  # -> Level 0
        0,                  # -> Level 1
        30 * minutes,       # -> Level 2
        4 * hours,          # -> Level 3
        8 * hours,          # -> Level 4
        1 * days,           # -> Level 5
        3 * days,           # -> Level 6
        7 * days,           # -> Level 7
        14 * days,          # -> Level 8
        30 * days,          # -> Level 9
        120 * days,         # -> Level 10
    ]

    return level_to_time[next_word_level]


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

        # Insert next reviews.
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

        # Insert next review.
        review_date = timezone.now() + timedelta(seconds=get_review_time(next_word_level=2))
        Review.objects.bulk_create(
            [Review(word_id=word_id, user_id=request.user.id, date=review_date) for word_id in word_ids]
        )

        return JsonResponse({})
    else:
        return HttpResponseNotFound()


def finish_review(request):
    if request.method == 'PUT':
        stats = json.loads(request.body.decode("utf-8"))
        print(stats)
        return JsonResponse({})
    else:
        return HttpResponseNotFound()