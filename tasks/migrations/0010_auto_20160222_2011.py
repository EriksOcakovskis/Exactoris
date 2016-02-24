# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20160219_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='work_log',
        ),
        migrations.AddField(
            model_name='worklog',
            name='task',
            field=models.ForeignKey(to='tasks.Task', default=1),
            preserve_default=False,
        ),
    ]
