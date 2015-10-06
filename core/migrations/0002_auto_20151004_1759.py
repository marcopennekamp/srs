# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='kanji_dependencies',
            field=models.ManyToManyField(to='core.Kanji'),
        ),
        migrations.AlterField(
            model_name='kanji',
            name='character',
            field=models.CharField(unique=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
