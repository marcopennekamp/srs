# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_word_unique_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='unique_key',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
