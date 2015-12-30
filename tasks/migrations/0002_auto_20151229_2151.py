# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='prerequisite',
            field=models.ForeignKey(to='tasks.Task', blank=True, null=True),
            preserve_default=True,
        ),
    ]
