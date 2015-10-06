from core.models import KnownKanji


def get_known_kanji_set(user_id, kanji_query):
    if kanji_query is None:
        known_kanji_query = KnownKanji.objects.filter(user_id=user_id)
    else:
        known_kanji_query = KnownKanji.objects.filter(user_id=user_id, kanji__in=kanji_query)
    return set(known_kanji_query.values_list('kanji__id', flat=True))
