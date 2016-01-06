# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20151229_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='last_edited',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='registered',
            field=models.DateTimeField(editable=False),
            preserve_default=True,
        ),
    ]
