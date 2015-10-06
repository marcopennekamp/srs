# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_knownkanji_wanikanilevel_wordlevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='KanjiCollection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('kanji_list', models.ManyToManyField(to='core.Kanji')),
            ],
        ),
        migrations.RemoveField(
            model_name='wanikanilevel',
            name='kanji_list',
        ),
        migrations.AddField(
            model_name='wanikanilevel',
            name='collection',
            field=models.ForeignKey(to='core.KanjiCollection', default=None),
            preserve_default=False,
        ),
    ]
