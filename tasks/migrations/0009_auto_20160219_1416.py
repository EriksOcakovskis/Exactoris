# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_auto_20160218_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worklog',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='work_log',
            field=models.ManyToManyField(blank=True, to='tasks.WorkLog', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='worklog',
            name='assigned_to',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
    ]
