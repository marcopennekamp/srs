# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151006_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='unique_key',
            field=models.CharField(max_length=50, default=''),
            preserve_default=False,
        ),
    ]
