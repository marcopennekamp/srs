from datetime import timedelta
from core.models import KnownKanji


DURATION_MINUTES = 60
DURATION_HOURS = 60 * DURATION_MINUTES
DURATION_DAYS = 24 * DURATION_HOURS
DURATION_WEEKS = 7 * DURATION_DAYS
DURATION_MONTHS = DURATION_DAYS * 30


def get_known_kanji_set(user_id, kanji_query):
    if kanji_query is None:
        known_kanji_query = KnownKanji.objects.filter(user_id=user_id)
    else:
        known_kanji_query = KnownKanji.objects.filter(user_id=user_id, kanji__in=kanji_query)
    return set(known_kanji_query.values_list('kanji__id', flat=True))


# Returns the time to the next review as a timedelta.
def get_review_time(next_word_level):

    level_to_time = [
        0,  # -> Level 0
        0,  # -> Level 1
        30 * DURATION_MINUTES,  # -> Level 2
        4 * DURATION_HOURS,  # -> Level 3
        8 * DURATION_HOURS,  # -> Level 4
        1 * DURATION_DAYS,  # -> Level 5
        3 * DURATION_DAYS,  # -> Level 6
        1 * DURATION_WEEKS,  # -> Level 7
        2 * DURATION_WEEKS,  # -> Level 8
        1 * DURATION_MONTHS,  # -> Level 9
        4 * DURATION_MONTHS,  # -> Level 10
    ]

    return timedelta(seconds=level_to_time[next_word_level])


def seconds_to_friendly_time_string(seconds):
    def floor_and_to_string(duration, name):
        time = int(seconds / duration)
        result = str(time) + ' ' + name
        if time != 1:
            result += 's'
        return result

    if seconds > DURATION_MONTHS:
        return floor_and_to_string(DURATION_MONTHS, 'month')
    elif seconds > DURATION_WEEKS:
        return floor_and_to_string(DURATION_WEEKS, 'week')
    elif seconds > DURATION_DAYS:
        return floor_and_to_string(DURATION_DAYS, 'day')
    elif seconds > DURATION_HOURS:
        return floor_and_to_string(DURATION_HOURS, 'hour')
    elif seconds > DURATION_MINUTES:
        return floor_and_to_string(DURATION_MINUTES, 'minute')
    elif seconds > 0:
        return '< 1 minute'
    else:
        return 'now'
