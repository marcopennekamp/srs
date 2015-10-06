from django.db import models
from django.contrib.auth.models import User


class Kanji(models.Model):
    character = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.character


# Associates a registration with all their known Kanji.
class KnownKanji(models.Model):
    kanji = models.ForeignKey(Kanji)
    user = models.ForeignKey(User)

    def __str__(self):
        return "user " + self.user.username + " knows " + self.kanji.character


class KanjiCollection(models.Model):
    name = models.CharField(max_length=200)
    kanji_list = models.ManyToManyField(Kanji)
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class WaniKaniLevel(models.Model):
    level = models.IntegerField()
    collection = models.ForeignKey(KanjiCollection)

    def __str__(self):
        return str(self.level)


class Word(models.Model):
    word = models.CharField(max_length=20)
    unique_key = models.CharField(max_length=50, unique=True)
    kanji_dependencies = models.ManyToManyField(Kanji)

    def __str__(self):
        return self.word


class WordReading(models.Model):
    reading = models.CharField(max_length=200)
    owner = models.ForeignKey(Word)

    def __str__(self):
        return self.reading


class WordMeaning(models.Model):
    meaning = models.CharField(max_length=200)
    owner = models.ForeignKey(Word)

    def __str__(self):
        return self.meaning


# There is no level for 'unavailable' words, which are words that didn't meet their dependencies yet.
# This is simply covered by the absence of a row in the DB.
class WordLevel(models.Model):
    # A level of 0 means that the word has been unlocked, but not yet learned.
    NOT_YET_LEARNED = 0
    MAX_LEVEL = 10

    # Fields.
    user = models.ForeignKey(User)
    word = models.ForeignKey(Word)
    level = models.IntegerField()

    def __str__(self):
        return "User " + self.user.username + " has the word " + self.word.word + " on level " + str(self.level)
