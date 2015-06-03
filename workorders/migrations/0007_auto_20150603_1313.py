# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0006_auto_20150603_1255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder',
            old_name='description',
            new_name='issue_description',
        ),
        migrations.AddField(
            model_name='workorder',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='Is the job finished?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workorder',
            name='solution_description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
