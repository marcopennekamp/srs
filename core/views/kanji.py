# kanji_list may be none, in which case all known kanji for the user are queried.
import json
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Count, F
from django.db.models.functions import Length
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from core.models import KnownKanji, KanjiCollection, Kanji, Word, WordLevel
from core.util import get_known_kanji_set


@login_required
def kanji_collection_detail(request, collection_id):
    collection = get_object_or_404(KanjiCollection, pk=collection_id)
    kanji_ids = list(collection.kanji_list.values_list('id', flat=True))
    known_kanji_set = get_known_kanji_set(request.user.id, collection.kanji_list.get_queryset())

    context = {'collection': collection, 'known_kanji_set': known_kanji_set, 'kanji_id_json': json.dumps(kanji_ids)}
    return render(request, 'kanji/collection/detail.html', context)


@login_required
def kanji_collection_list(request, category):
    if category is None:
        collection_query = KanjiCollection.objects
    else:
        collection_query = KanjiCollection.objects.filter(category=category)

    kanji_query = collection_query.values_list('kanji_list')
    known_kanji_set = get_known_kanji_set(request.user.id, kanji_query)

    context = {'collection_list': collection_query.all(), 'known_kanji_set': known_kanji_set}
    return render(request, 'kanji/collection/list.html', context)


@login_required
def kanji_collection_list_all(request):
    return kanji_collection_list(request, None)


@login_required
def kanji_detail(request, kanji_id):
    kanji = get_object_or_404(Kanji, pk=kanji_id)
    is_known = KnownKanji.objects.filter(kanji_id=kanji_id, user_id=request.user.id).first() is not None
    context = {'kanji': kanji, 'is_known': is_known}
    return render(request, 'kanji/detail.html', context)


@login_required
def kanji_list(request):
    kanjis = Kanji.objects.all()
    known_kanji_set = get_known_kanji_set(request.user.id, None)

    context = {'kanji_list': kanjis, 'known_kanji_set': known_kanji_set}
    return render(request, 'kanji/list.html', context)


def unlock_words(user_id, kanji_id_list):
    # The number of known Kanji from the set of dependencies.
    known_count_query_str = """
        (
          SELECT COUNT(*) FROM "core_word_kanji_dependencies" AS dependency
          JOIN "core_knownkanji" AS known_kanji
          ON known_kanji."kanji_id" = dependency."kanji_id" AND known_kanji."user_id" = %(user_id)s
          WHERE dependency."word_id" = word."id"
        )
    """

    # The total number of dependencies.
    dependency_count_query_str = """
        (
            SELECT COUNT(*) FROM "core_word_kanji_dependencies" AS dependency
            WHERE dependency."word_id" = word."id"
        )
    """

    word_query_str = """
            WITH
                user_word_level AS
                    (SELECT * FROM "core_wordlevel" AS word_level WHERE word_level."user_id" = %(user_id)s)
            SELECT
                word."id", word."word", word."unique_key",
                """ + dependency_count_query_str + """ AS dependency_count,
                """ + known_count_query_str + """ AS known_count
            FROM "core_word" AS word
            WHERE (
                -- Only search for words with the affected Kanji.
                EXISTS (
                    SELECT 1 FROM "core_word_kanji_dependencies" AS search_dependencies
                    WHERE search_dependencies."word_id" = word."id"
                      AND search_dependencies."kanji_id" = ANY(%(kanji_ids)s)
                )

                -- Only search for words that are not yet unlocked.
            AND NOT EXISTS (SELECT 1 FROM user_word_level WHERE user_word_level."word_id"=word."id")

                -- Only choose the word if all dependencies have been fulfilled.
            AND """ + dependency_count_query_str + """ = """ + known_count_query_str + """
            )
        """

    cursor = connection.cursor()
    cursor.execute(word_query_str, {
            'user_id': str(user_id),
            'kanji_ids': kanji_id_list,
        })
    print(cursor.fetchone())

    word_query = Word.objects.raw(
        word_query_str,
        {
            'user_id': str(user_id),
            'kanji_ids': kanji_id_list,
        }
    )

    print("Unlock the following words:")
    for word in word_query:
        print(str(word) + ': ' + str(word.known_count) + '/' + str(word.dependency_count))

    WordLevel.objects.bulk_create(
        [WordLevel(user_id=user_id, word=word, level=WordLevel.NOT_YET_LEARNED) for word in word_query]
    )


def lock_unlearned_words(user_id, kanji_id_list):
    word_query = (
        # Get any words where at least one Kanji has been locked.
        Word.objects.filter(kanji_dependencies__id__in=kanji_id_list)
    )

    level_query = WordLevel.objects.filter(user_id=user_id).filter(word__in=word_query).filter(level__lt=1)

    print("Lock the following words:")
    for word_level in level_query.all():
        print(str(word_level.word))

    level_query.delete()


@login_required
def mark_kanji(request):
    if request.method == 'PUT':
        kanji_id_list = json.loads(request.body.decode("utf-8"))

        known_kanjis = KnownKanji.objects.filter(user_id=request.user.id, kanji_id__in=kanji_id_list).all()
        for known_kanji in known_kanjis:
            kanji_id_list.remove(known_kanji.kanji_id)

        # Only continue if the list has at least one element.
        if kanji_id_list:
            # TODO: Save all objects at the same time?
            for kanji_id in kanji_id_list:
                known_kanji = KnownKanji(kanji_id=kanji_id, user=request.user)
                known_kanji.save()

            # This needs to be called after all the known Kanji are saved!
            unlock_words(request.user.id, kanji_id_list)

        return HttpResponse('{}')
    else:
        return HttpResponseNotFound()


@login_required
def unmark_kanji(request):
    if request.method == 'PUT':
        kanji_id_list = json.loads(request.body.decode("utf-8"))

        # Just delete all those entries.
        KnownKanji.objects.filter(user_id=request.user.id, kanji_id__in=kanji_id_list).delete()
        lock_unlearned_words(request.user.id, kanji_id_list)

        return HttpResponse('{}')
    else:
        return HttpResponseNotFound()
