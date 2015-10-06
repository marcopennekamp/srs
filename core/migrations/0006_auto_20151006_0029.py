# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_kanjicollection_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordMeaning',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('meaning', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WordMeaningSet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('word', models.ForeignKey(to='core.Word')),
            ],
        ),
        migrations.AddField(
            model_name='wordmeaning',
            name='owning_set',
            field=models.ForeignKey(to='core.WordMeaningSet'),
        ),
    ]
