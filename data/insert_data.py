import csv
from core.models import Kanji, WaniKaniLevel, KanjiCollection, Word, WordReading, WordMeaning


def read_word_list(path):
    with open(path) as f:
        word_list = f.readlines()
    return [word.strip('\n') for word in word_list] # Strip all newlines.


def add_to_collection(collection, kanji_list):
    for kanji_character in kanji_list:
        # It is possible that the Kanji is already in the database, in which case
        # we only need to add exactly that Kanji to the collection.
        existing_kanji = Kanji.objects.filter(character=kanji_character).first()
        if existing_kanji is None:
            kanji = Kanji(character=kanji_character)
            kanji.save()
        else:
            kanji = existing_kanji
        collection.kanji_list.add(kanji)


# Automatically checks if the levels are already present.
def insert_wanikani_kanji():
    max_level = 60
    for level in range(1, max_level + 1):
        if WaniKaniLevel.objects.filter(level=level).count() > 0:
            #print('Skipping WaniKani Level ' + str(level) + ': Already present.')
            continue

        kanji_list = read_word_list('kanji/wanikani/level' + str(level) + '.kanji')
        collection = KanjiCollection(name='WaniKani Level ' + str(level), category='wanikani')
        collection.save()
        wanikani_level = WaniKaniLevel(level=level, collection=collection)
        wanikani_level.save()
        add_to_collection(collection, kanji_list)
        print('Added collection: ' + collection.name)


# Automatically checks if the collections are already present.
def insert_jlpt_kanji():
    for level in range(5, 0, -1):
        collection_name = 'JLPT N' + str(level)
        if KanjiCollection.objects.filter(name=collection_name).count() > 0:
            #print('Skipping JLPT N' + str(level) + ': Already present.')
            continue

        kanji_list = read_word_list('kanji/jlpt/n' + str(level) + '.kanji')
        collection = KanjiCollection(name=collection_name, category='jlpt')
        collection.save()
        add_to_collection(collection, kanji_list)
        print('Added collection: ' + collection_name)


# Just tests for CJK Unified Ideographs
def is_kanji(char):
    ordinal = ord(char)
    return 0x4e00 < ordinal < 0x9fff or 0x3400 < ordinal < 0x4dff


def add_kanji_dependencies(word):
    for char in word.word:
        if is_kanji(char):
            kanji = Kanji.objects.filter(character=char).first()
            if kanji is None:
                kanji = Kanji(character=char)
                kanji.save()
            word.kanji_dependencies.add(kanji)


def insert_core6k_words():
    with open('words/words.csv') as core_file:
        reader = csv.DictReader(core_file)
        for row in reader:
            word_str = row['word']
            readings = [reading.strip() for reading in row['readings'].split(',')]
            meanings = [meaning.strip() for meaning in row['meanings'].split(',')]
            unique_key = row['unique-key']

            # Check if word with same unique key already exists.
            word = Word.objects.filter(unique_key=unique_key).first()
            if word is None:
                word = Word(word=word_str, unique_key=unique_key)
                word.save()
                add_kanji_dependencies(word)
                for reading in readings:
                    word_reading = WordReading(reading=reading, owner=word)
                    word_reading.save()
                for meaning in meanings:
                    word_meaning = WordMeaning(meaning=meaning, owner=word)
                    word_meaning.save()
                print('Added word with unique key: ' + unique_key)


insert_wanikani_kanji()
insert_jlpt_kanji()
insert_core6k_words()


