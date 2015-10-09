# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20151008_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordmeaning',
            name='owner',
            field=models.ForeignKey(to='core.Word', related_name='meanings'),
        ),
        migrations.AlterField(
            model_name='wordreading',
            name='owner',
            field=models.ForeignKey(to='core.Word', related_name='readings'),
        ),
    ]
