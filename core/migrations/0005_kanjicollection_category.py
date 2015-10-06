# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151004_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanjicollection',
            name='category',
            field=models.CharField(default='wanikani', max_length=200),
            preserve_default=False,
        ),
    ]
