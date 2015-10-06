# kanji_list may be none, in which case all known kanji for the user are queried.
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from core.models import KnownKanji, KanjiCollection, Kanji
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


@login_required
def mark_kanji(request):
    if request.method == 'PUT':
        kanji_id_list = json.loads(request.body.decode("utf-8"))

        known_kanjis = KnownKanji.objects.filter(user_id=request.user.id, kanji_id__in=kanji_id_list).all()
        db_known_set = set()
        for known_kanji in known_kanjis:
            db_known_set.add(known_kanji.kanji_id)

        for kanji_id in kanji_id_list:
            # TODO: Save all objects at the same time?
            known_kanji = KnownKanji(kanji_id=kanji_id, user=request.user)
            known_kanji.save()

        return HttpResponse('{}')
    else:
        return HttpResponseNotFound()


@login_required
def unmark_kanji(request):
    if request.method == 'PUT':
        kanji_id_list = json.loads(request.body.decode("utf-8"))

        # Just delete all those entries.
        KnownKanji.objects.filter(user_id=request.user.id, kanji_id__in=kanji_id_list).delete()

        return HttpResponse('{}')
    else:
        return HttpResponseNotFound()