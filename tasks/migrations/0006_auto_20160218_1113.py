# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20160114_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[(1, 'In progress'), (2, 'Overdue'), (3, 'On hold'), (4, 'Done'), (5, 'To-Do')], max_length=2, default=5),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
