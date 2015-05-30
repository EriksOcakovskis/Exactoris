# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0004_auto_20150416_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workorder',
            name='time_elapsed',
        ),
    ]
