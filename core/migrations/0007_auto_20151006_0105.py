# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151006_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordReading',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('reading', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='wordmeaningset',
            name='word',
        ),
        migrations.RemoveField(
            model_name='wordmeaning',
            name='owning_set',
        ),
        migrations.AddField(
            model_name='wordmeaning',
            name='owner',
            field=models.ForeignKey(default=None, to='core.Word'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='WordMeaningSet',
        ),
        migrations.AddField(
            model_name='wordreading',
            name='owner',
            field=models.ForeignKey(to='core.Word'),
        ),
    ]
