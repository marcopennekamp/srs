# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='time',
            new_name='date',
        ),
    ]
