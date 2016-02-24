# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20160218_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='typeof_recurrence',
            field=models.IntegerField(max_length=2, choices=[(1, 'Yearly'), (2, 'Monthly'), (3, 'Weekly'), (4, 'Daily')], blank=True, null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='RecurrenceType',
        ),
    ]
